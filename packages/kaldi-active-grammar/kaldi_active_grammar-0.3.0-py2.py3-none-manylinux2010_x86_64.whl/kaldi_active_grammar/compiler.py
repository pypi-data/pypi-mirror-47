#
# This file is part of kaldi-active-grammar.
# (c) Copyright 2019 by David Zurow
# Licensed under the AGPL-3.0, with exceptions; see LICENSE.txt file.
#

import base64, collections, logging, os.path, re, shlex, subprocess

from . import _log, KaldiError
from .utils import debug_timer, find_file, platform, symbol_table_lookup, FileCache
import utils
from .wfst import WFST

import cloud

_log = _log.getChild('compiler')


########################################################################################################################

class KaldiRule(object):
    def __init__(self, compiler, id, name, nonterm=True, has_dictation=None):
        self.compiler = compiler
        self.id = int(id)  # matches "nonterm:rule__"; 0-based
        self.name = name
        if self.id > self.compiler._max_rule_id: raise KaldiError("KaldiRule id > compiler._max_rule_id")
        self.nonterm = nonterm
        self.has_dictation = has_dictation
        self.fst = WFST()
        self.matcher = None
        self.active = True

    def __str__(self):
        return "KaldiRule(%s, %s)" % (self.id, self.name)

    decoder = property(lambda self: self.compiler.decoder)
    filename = property(lambda self: base64.b16encode(self.name) + '.fst')  # FIXME: need to handle unicode?
    filepath = property(lambda self: os.path.join(self.compiler.tmp_dir, self.filename))

    def compile_file(self):
        _log.debug("%s: Compiling exported rule %r to %s" % (self, self.name, self.filename))

        if self.filename in self.compiler._fst_filenames_set:
            raise KaldiError("KaldiRule fst filename collision %r. Duplicate grammar/rule name %r?" % (self.filename, self.name))
        self.compiler._fst_filenames_set.add(self.filename)

        fst_text = self.fst.fst_text
        if self.compiler.fst_cache.contains(self.filename, fst_text) and os.path.exists(self.filepath) and True or False:
            # _log.debug("%s: Skipped full compilation thanks to FileCache" % self)
            return
        else:
            # _log.info("%s: FileCache useless; has %s not %s" % (self,
            #     self.compiler.fst_cache.hash(self.compiler.fst_cache.cache[self.filename]) if self.filename in self.compiler.fst_cache.cache else None,
            #     self.compiler.fst_cache.hash(fst_text)))
            pass
        with open(self.filepath + '.txt', 'w') as f:
            f.write(fst_text)

        if self.compiler.decoding_framework == 'agf':
            self.compiler._compile_agf_graph(fstcompile=True, nonterm=self.nonterm, filename=self.filepath)
        elif self.compiler.decoding_framework == 'otf':
            self.compiler._compile_otf_graph(filename=self.filepath)

        self.compiler.fst_cache.add(self.filename, fst_text)

    def load(self):
        self.decoder.add_grammar_fst(self.filepath)

    def destroy(self):
        self.decoder.remove_grammar_fst(self.id)
        self.compiler._fst_filenames_set.remove(self.filename)
        # Adjust kaldi_rules ids down, if above self.id
        for kaldi_rule in self.compiler.kaldi_rule_by_id_dict.values():
            if kaldi_rule.id > self.id:
                kaldi_rule.id -= 1
        # Rebuild dict
        self.compiler.kaldi_rule_by_id_dict = { kaldi_rule.id: kaldi_rule for kaldi_rule in self.compiler.kaldi_rule_by_id_dict.values() }
        self.compiler.free_rule_id()


########################################################################################################################

class Compiler(object):

    def __init__(self, model_dir, tmp_dir=None):
        self.decoder = None
        self.decoding_framework = 'agf'
        assert self.decoding_framework in ('otf', 'agf')
        self.parsing_framework = 'token'
        assert self.parsing_framework in ('text', 'token')

        self.exec_dir = os.path.join(utils.exec_dir, '')
        self.model_dir = os.path.join(model_dir or '', '')
        self.tmp_dir = os.path.join(tmp_dir or 'kaldi_tmp', '')
        if not os.path.exists(self.exec_dir): raise KaldiError("cannot find exec_dir: %r" % self.exec_dir)
        if not os.path.exists(self.model_dir): raise KaldiError("cannot find model_dir: %r" % self.model_dir)
        if not os.path.exists(self.tmp_dir):
            _log.warning("%s: creating tmp dir: %r" % (self, self.tmp_dir))
            os.mkdir(self.tmp_dir)

        self.files_dict = {
            'exec_dir': self.exec_dir,
            'model_dir': self.model_dir,
            'tmp_dir': self.tmp_dir,
            'words.txt': find_file(self.model_dir, 'words.txt'),
            'phones.txt': find_file(self.model_dir, 'phones.txt'),
            'disambig.int': find_file(self.model_dir, 'disambig.int'),
            'L_disambig.fst': find_file(self.model_dir, 'L_disambig.fst'),
            'tree': find_file(self.model_dir, 'tree'),
            '1.mdl': find_file(self.model_dir, '1.mdl'),
            'final.mdl': find_file(self.model_dir, 'final.mdl'),
            'g.irelabel': find_file(self.model_dir, 'g.irelabel'),  # otf
        }
        self.files_dict.update({ k.replace('.', '_'): v for k, v in self.files_dict.items() })  # for named placeholder access in str.format()
        self.fst_cache = FileCache(os.path.join(self.tmp_dir, 'fst_cache.json'), dependencies_dict=self.files_dict)

        self._num_kaldi_rules = 0
        self.kaldi_rule_by_id_dict = collections.OrderedDict()  # maps KaldiRule.id -> KaldiRule
        self._fst_filenames_set = set()
        self._lexicon_words = set()

    _max_rule_id = 999
    num_kaldi_rules = property(lambda self: self._num_kaldi_rules)
    nonterminals = tuple(['#nonterm:dictation'] + ['#nonterm:rule%i' % i for i in range(_max_rule_id + 1)])

    default_dictation_g_filepath = property(lambda self: os.path.join(self.model_dir, 'G_dictation.fst'))
    _dictation_fst_filepath = property(lambda self: os.path.join(self.model_dir, 'Dictation.fst'))

    def load_words(self, words_file=None, unigram_probs_file=None):
        if words_file is None: words_file = self.files_dict['words.txt']
        _log.debug("loading words from %r", words_file)
        with open(words_file, 'r') as file:
            word_id_pairs = [line.strip().split() for line in file]
        self._lexicon_words = set([word for word, id in word_id_pairs
            if word.lower() not in "<eps> !SIL <UNK> #0 <s> </s>".lower().split() and not word.startswith('#nonterm')])

        if unigram_probs_file:
            with open(unigram_probs_file, 'r') as file:
                word_count_pairs = [line.strip().split() for line in file]
            word_count_pairs = [(word, int(count)) for word, count in word_count_pairs[:30000] if word in self._lexicon_words]
            total = sum(count for word, count in word_count_pairs)
            self._lexicon_word_probs = {word: (float(count) / total) for word, count in word_count_pairs}

        self._longest_word = max(self._lexicon_words, key=len)

        return self._lexicon_words

    def alloc_rule_id(self):
        id = self._num_kaldi_rules
        self._num_kaldi_rules += 1
        return id

    def free_rule_id(self):
        id = self._num_kaldi_rules
        self._num_kaldi_rules -= 1
        return id

    ####################################################################################################################
    # Methods for compiling graphs.

    def _compile_otf_graph(self, **kwargs):
        # FIXME: documentation
        with debug_timer(_log.debug, "otf graph compilation"):
            format_kwargs = dict(self.files_dict, **kwargs)
            def run(cmd, **kwargs):
                with debug_timer(_log.debug, "otf graph compilation step", False):
                    args = shlex.split(cmd.format(**format_kwargs), posix=(platform != 'windows'))
                    _log.log(5, "subprocess.check_call(%r)", args)
                    subprocess.check_call(args, **kwargs)

            p1 = run("{exec_dir}fstcompile --isymbols={words_txt} --osymbols={words_txt} {filename}.txt {filename}")
            p2 = run("{exec_dir}fstrelabel --relabel_ipairs={g.irelabel} {filename} {filename}")
            p3 = run("{exec_dir}fstarcsort {filename} {filename}")
            # p4 = run("{exec_dir}fstconvert --fst_type=const {filename} {filename}")

    def _compile_agf_graph(self, fstcompile=False, nonterm=False, in_filename=None, filename=None, **kwargs):
        # FIXME: documentation
        with debug_timer(_log.debug, "agf graph compilation"):
            in_filename = in_filename or filename
            verbose_level = 5 if _log.isEnabledFor(5) else 0
            format_kwargs = dict(self.files_dict, in_filename=in_filename, filename=filename, verbose=verbose_level, **kwargs)
            format_kwargs.update(nonterm_phones_offset = symbol_table_lookup(format_kwargs['phones.txt'], '#nonterm_bos'))
            if format_kwargs['nonterm_phones_offset'] is None:
                raise KaldiError("cannot find #nonterm_bos symbol in phones.txt")
            def run(cmd, **kwargs):
                with debug_timer(_log.debug, "agf graph compilation step", False), open(os.devnull, 'w') as devnull:
                    output = None if _log.isEnabledFor(logging.DEBUG) else devnull
                    args = shlex.split(cmd.format(**format_kwargs), posix=(platform != 'windows'))
                    _log.log(5, "subprocess.check_call(%r)", args)
                    subprocess.check_call(args, stdout=output, stderr=output, **kwargs)
                    format_kwargs.update(in_filename=filename)

            if fstcompile: run("{exec_dir}fstcompile --isymbols={words_txt} --osymbols={words_txt} {in_filename}.txt {filename}")
            # run("cp {in_filename} {filename}-G")
            if nonterm: run("{exec_dir}fstconcat {tmp_dir}nonterm_begin.fst {in_filename} {filename}")
            if nonterm: run("{exec_dir}fstconcat {in_filename} {tmp_dir}nonterm_end.fst {filename}")
            if fstcompile: run("{exec_dir}fstarcsort --sort_type=ilabel {in_filename} {filename}")
            # run("cp {in_filename} {filename}-G")
            run("{exec_dir}compile-graph --nonterm-phones-offset={nonterm_phones_offset} --read-disambig-syms={disambig_int} --verbose={verbose}"
                + " {tree} {final_mdl} {L_disambig_fst} {in_filename} {filename}")

    def _compile_base_fsts(self):
        format_kwargs = dict(self.files_dict)
        def run(cmd): subprocess.check_call(cmd.format(**format_kwargs), shell=True)  # FIXME: unsafe shell?
        # FIXME: check for existing before generating?
        if platform == 'windows':
            run("(echo 0 1 #nonterm_begin 0^& echo 1) | {exec_dir}fstcompile.exe --isymbols={words_txt} > {tmp_dir}nonterm_begin.fst")
            run("(echo 0 1 #nonterm_end 0^& echo 1) | {exec_dir}fstcompile.exe --isymbols={words_txt} > {tmp_dir}nonterm_end.fst")
        else:
            run("(echo 0 1 \\#nonterm_begin 0; echo 1) | {exec_dir}fstcompile --isymbols={words_txt} > {tmp_dir}nonterm_begin.fst")
            run("(echo 0 1 \\#nonterm_end 0; echo 1) | {exec_dir}fstcompile --isymbols={words_txt} > {tmp_dir}nonterm_end.fst")

    def compile_top_fst(self):
        kaldi_rule = KaldiRule(self, -1, 'top', nonterm=False)
        fst = kaldi_rule.fst
        state_initial = fst.add_state(initial=True)
        state_final = fst.add_state(final=True)
        for i in range(self._max_rule_id + 1):
            # fst.add_arc(state_initial, state_final, '#nonterm:rule'+str(i), olabel=WFST.eps)
            fst.add_arc(state_initial, state_final, '#nonterm:rule'+str(i), olabel='#nonterm:rule'+str(i))
        fst.equalize_weights()
        kaldi_rule.compile_file()
        return kaldi_rule

    def _get_dictation_fst_filepath(self):
        if os.path.exists(self._dictation_fst_filepath):
            return self._dictation_fst_filepath
        _log.error("cannot find dictation fst: %s", self._dictation_fst_filepath)
        # _log.error("using universal dictation fst")
    dictation_fst_filepath = property(_get_dictation_fst_filepath)

    # def _construct_dictation_states(self, fst, src_state, dst_state, number=(1,None), words=None, start_weight=None):
    #     """
    #     Matches `number` words.
    #     :param number: (0,None) or (1,None) or (1,1), where None is infinity.
    #     """
    #     # unweighted=0.01
    #     if words is None: words = self._lexicon_words
    #     word_probs = self._lexicon_word_probs
    #     backoff_state = fst.add_state()
    #     fst.add_arc(src_state, backoff_state, None, weight=start_weight)
    #     if number[0] == 0:
    #         fst.add_arc(backoff_state, dst_state, None)
    #     for word, prob in word_probs.items():
    #         state = fst.add_state()
    #         fst.add_arc(backoff_state, state, word, weight=prob)
    #         if number[1] == None:
    #             fst.add_arc(state, backoff_state, None)
    #         fst.add_arc(state, dst_state, None)

    def compile_universal_grammar(self, words=None):
        """recognizes any sequence of words"""
        kaldi_rule = KaldiRule(self, -1, 'universal')
        if words is None: words = self._lexicon_words
        fst = kaldi_rule.fst
        backoff_state = fst.add_state(initial=True, final=True)
        for word in words:
            # state = fst.add_state()
            # fst.add_arc(backoff_state, state, word)
            # fst.add_arc(state, backoff_state, None)
            fst.add_arc(backoff_state, backoff_state, word)
        kaldi_rule.compile_file()
        return kaldi_rule

    def compile_dictation_fst(self, g_filename):
        self._compile_agf_graph(in_filename=g_filename, filename=self._dictation_fst_filepath, nonterm=True)

    ####################################################################################################################
    # Methods for recognition.

    def prepare_for_recognition(self):
        self.fst_cache.save()

    def parse_output_for_rule(self, kaldi_rule, output):
        # Can be used even when self.parsing_framework == 'token', only for mimic (which contains no nonterms)
        try:
            parse_results = kaldi_rule.matcher.parseString(output, parseAll=True)
        except pp.ParseException:
            return None
        parsed_output = ' '.join(parse_results)
        if parsed_output.lower() != output:
            self._log.error("parsed_output(%r).lower() != output(%r)" % (parse_results, output))
        kaldi_rule_id = int(parse_results.getName())
        assert kaldi_rule_id == kaldi_rule.id
        return parsed_output

    cloud_dictation = True
    cloud_dictation_regex = re.compile(r'#nonterm:dictation_cloud (.*?) #nonterm:end')

    def parse_output(self, output, dictation_info_func=None):
        assert self.parsing_framework == 'token'
        self._log.debug("parse_output(%r)" % output)
        if output == '':
            return None, ''

        nonterm_token, _, parsed_output = output.partition(' ')
        assert nonterm_token.startswith('#nonterm:rule')
        kaldi_rule_id = int(nonterm_token[len('#nonterm:rule'):])
        kaldi_rule = self.kaldi_rule_by_id_dict[kaldi_rule_id]

        if self.cloud_dictation and dictation_info_func and kaldi_rule.has_dictation and '#nonterm:dictation_cloud' in parsed_output:
            audio_data, word_align = dictation_info_func()
            words, times, lengths = zip(*word_align)
            dictation_spans = [{
                    'index_start': index,
                    'offset_start': time,
                    'index_end': words.index('#nonterm:end', index),
                    'offset_end': times[words.index('#nonterm:end', index)],
                }
                for index, (word, time, length) in zip(range(len(word_align)), word_align)
                if word.startswith('#nonterm:dictation_cloud')]

            # If last dictation is at end of utterance, include rest of audio_data; else, include half of audio_data between dictation end and start of next word
            dictation_span = dictation_spans[-1]
            if dictation_span['index_end'] == len(word_align) - 1:
                dictation_span['offset_end'] = len(audio_data)
            else:
                next_word_time = times[dictation_span['index_end'] + 1]
                dictation_span['offset_end'] = (dictation_span['offset_end'] + next_word_time) / 2

            def replace_dictation(matchobj):
                orig_text = matchobj.group(1)
                dictation_span = dictation_spans.pop(0)
                dictation_audio = audio_data[dictation_span['offset_start'] : dictation_span['offset_end']]
                with debug_timer(self._log.debug, 'cloud dictation call'):
                    cloud_text = cloud.GCloud.transcribe_data_sync(dictation_audio)
                    self._log.debug("cloud_dictation: %.2fs audio -> %r", (0.5 * len(dictation_audio) / 16000), cloud_text)
                # with debug_timer(self._log.debug, 'cloud dictation call'):
                #     cloud_text = cloud.GCloud.transcribe_data_sync(dictation_audio, model='command_and_search')
                #     self._log.debug("cloud_dictation: %.2fs audio -> %r", (0.5 * len(dictation_audio) / 16000), cloud_text)
                # with debug_timer(self._log.debug, 'cloud dictation call'):
                #     cloud_text = cloud.GCloud.transcribe_data_streaming(dictation_audio)
                #     self._log.debug("cloud_dictation: %.2fs audio -> %r", (0.5 * len(dictation_audio) / 16000), cloud_text)
                # cloud.write_wav('test.wav', dictation_audio)
                return cloud_text or orig_text

            parsed_output = self.cloud_dictation_regex.sub(replace_dictation, parsed_output)

        parsed_output = remove_nonterms(parsed_output)
        return kaldi_rule, parsed_output

########################################################################################################################
# Utility functions.

def remove_nonterms(text):
    return ' '.join(word for word in text.split() if not word.startswith('#nonterm:'))
