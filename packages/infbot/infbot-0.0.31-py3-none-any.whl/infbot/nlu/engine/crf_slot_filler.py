# -*- coding: utf-8 -*-
"""
使用sklearn-crfsuite进行NER识别

python3 -m lu.engine.crf_slot_filler

"""

# import os
import re
from copy import deepcopy
from urllib.parse import quote, unquote
import numpy as np
from sklearn_crfsuite import CRF, metrics
# from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_validate
from .engine_core import EngineCore
from infbot.logger import logger


def single_sentence_to_features(sentence):
    """转换单个句子的特征"""
    sentence = [x.lower() for x in sentence]
    features = []
    for i, token in enumerate(sentence):
        # token = sentence[i]
        token_prev_3 = '_' if i - 3 < 0 else sentence[i - 3]
        token_prev_2 = '_' if i - 2 < 0 else sentence[i - 2]
        token_prev = '_' if i == 0 else sentence[i - 1]
        token_next = '_' if i == (len(sentence) - 1) else sentence[i + 1]
        token_next_2 = '_' if (i + 2) >= len(sentence) else sentence[i + 2]
        token_next_3 = '_' if (i + 3) >= len(sentence) else sentence[i + 3]
        feature = {
            'bias':
            1.0,
            'BOS':
            True if i == 0 else False,
            'EOS':
            True if i == (len(sentence) - 1) else False,
            'token-3':
            token_prev_3,
            'token-2':
            token_prev_2,
            'token-1':
            token_prev,
            'token':
            token,
            'token+1':
            token_next,
            'token+2':
            token_next_2,
            'token+3':
            token_next_3,
            'token-3:token-2':
            token_prev_3 + token_prev_2,
            'token-2:token-1':
            token_prev_2 + token_prev,
            'token-1:token':
            token_prev + token,
            'token:token+1':
            token + token_next,
            'token+1:token+2':
            token_next + token_next_2,
            'token+2:token+3':
            token_next_2 + token_next_3,
            'isEnglishChar':
            True if re.match(r'[a-zA-Z]', token) else False,
            'isNumberChar':
            True if re.match(r'[0-9]', token) else False,
            'isChineseNumberChar':
            True if re.match(r'[一二三四五六七八九十零俩仨]', token) else False,
            'isChineseChar':
            True if re.match(r'[\u4e00-\u9ffff]', token) else False,
            'isChinesePunctuationChar':
            True if re.match(r'[，。？！：；《》]', token) else False,
            'isChinesePunctuationChar-1':
            True if re.match(r'[，。？！：；《》]', token_prev) else False,
            'isChinesePunctuationChar+1':
            True if re.match(r'[，。？！：；《》]', token_next) else False,
        }
        features.append(feature)
    return features


def sentences_to_features(sentence_result):
    """把句子们转换为特征"""
    x_train = []
    for s in sentence_result:
        x_train.append(single_sentence_to_features(s))
    return x_train


def get_slots(sentence, slot):
    """转换结果"""
    current = None
    current_str = []
    ret = []
    for s, ss in zip(sentence, slot):
        if ss != 'O':
            ss = ss[2:]
            if current is None:
                current = ss
                current_str = [s]
            else:
                if current == ss:
                    current_str.append(s)
                else:
                    ret.append((current, ''.join(current_str)))
                    current = ss
                    current_str = []
        else:

            # 应对 B1 O B1 的情况，B1和B1很可能是连续的，而O是空格
            if (s == ' ' or s == '　'):
                continue

            if current is not None:
                ret.append((current, ''.join(current_str)))
                current = None
                current_str = []

    if current is not None:
        ret.append((current, ''.join(current_str)))

    ret_dict = {}
    for s, v in ret:
        if s not in ret_dict:
            ret_dict[s] = []
        ret_dict[s].append(v)
    return ret_dict


def get_slots_detail(sentence, slot):
    """
    example:
    sentence == ['买', '2', '手']
    slot == ['O', 'B_number', 'O']
    """
    current = None
    current_str = []
    ret = []
    i = 0
    for i, (s, ss) in enumerate(zip(sentence, slot)):
        if ss != 'O':
            ss = ss[2:]
            if current is None:
                current = ss
                current_str = [s]
            else:
                if current == ss:
                    current_str.append(s)
                else:
                    ret.append((current, ''.join(current_str),
                                i - len(current_str), i))
                    current = ss
                    current_str = [s]
        else:
            if current is not None:
                ret.append((current, ''.join(current_str),
                            i - len(current_str), i))
                current = None
                current_str = []

    if current is not None:
        ret.append((current, ''.join(current_str), i - len(current_str), i))

    ret_list = []
    for s, v, start, end in ret:
        ret_list.append({'slot_name': s, 'slot_value': v, 'pos': (start, end)})
    return ret_list


def get_exact_right(slot_true, slot_pred):
    import json
    for s, v in slot_true.items():
        if s not in slot_pred:
            return False
        v = json.dumps(v)
        vp = json.dumps(slot_pred[s])
        if v != vp:
            return False
    return True


class CRFSlotFiller(EngineCore):
    """注意文本都会变小写"""

    def __init__(self):
        """初始化"""
        super(CRFSlotFiller, self).__init__(
            domain_implement=False,
            intent_implement=False,
            slot_implement=True)
        self.crf = None

    def fit(self,
            sentence_result,
            slot_result,
            max_iterations=100,
            c1=0.17,
            c2=0.01):
        """fit model"""

        self.c1 = c1
        self.c2 = c2
        self.max_iterations = max_iterations

        logger.info('fit CRFSlotFiller')

        x_train = sentences_to_features(sentence_result)
        y_train = deepcopy(slot_result)
        labels = set()
        for x in slot_result:
            labels.update(x)
        labels = sorted(list(labels))
        labels.remove('O')
        all_labels = ', '.join(labels)
        logger.info('labels: %s', all_labels)
        self.labels = labels

        logger.info(f'x_train %s, y_train %s', len(x_train), len(y_train))
        for i, (x, y) in enumerate(zip(x_train, y_train)):
            assert len(x) == len(y), '"{}", "{}" diff'.format(
                str([xx['token'] for xx in x]), str(y))
            # fix Chinese
            y_train[i] = [quote(j) for j in y]

        # if os.environ.get('CRF') == 'search':
        # crf = CRF(
        #     algorithm='lbfgs',
        #     max_iterations=50,
        #     all_possible_transitions=True)
        # params_space = {
        #     'c1': scipy.stats.expon(scale=0.5),
        #     'c2': scipy.stats.expon(scale=0.05),
        # }
        # f1_score = make_scorer(
        #     metrics.flat_f1_score, average='weighted', labels=labels)
        # rs = RandomizedSearchCV(
        #     crf,
        #     params_space,
        #     cv=3,
        #     verbose=1,
        #     n_jobs=2,
        #     n_iter=8 * 8,
        #     scoring=f1_score)
        # rs.fit(x_train, y_train)
        # logger.info('best params: %s', rs.best_params_)
        # logger.info('best cv score: %s', rs.best_score_)
        # self.crf = rs.best_estimator_
        # else:

        crf = CRF(
            algorithm='lbfgs',
            c1=c1,
            c2=c2,
            max_iterations=max_iterations,
            all_possible_transitions=True)
        crf.fit(x_train, y_train)

        self.crf = crf

    def predict_slot(self, nlu_obj):
        """识别实体"""
        tokens = nlu_obj['tokens']
        tokens = [x.lower() for x in tokens]
        ret = self.predict([tokens])
        crf_ret = get_slots_detail(nlu_obj['tokens'], ret[0])
        nlu_obj['crf_slot_filler'] = {'slots': crf_ret}
        for slot in crf_ret:
            slot['from'] = 'crf_slot_filler'
        if len(nlu_obj['slots']) <= 0:
            nlu_obj['slots'] = crf_ret
        else:
            for slot in crf_ret:
                is_include = False
                for s in nlu_obj['slots']:
                    if slot['pos'][0] >= s['pos'][0] and slot['pos'][0] <= s[
                            'pos'][1]:
                        is_include = True
                        break
                    elif slot['pos'][1] >= s['pos'][0] and slot['pos'][1] <= s[
                            'pos'][1]:
                        is_include = True
                        break
                    elif s['pos'][0] >= slot['pos'][0] and s['pos'][0] <= slot[
                            'pos'][1]:
                        is_include = True
                        break
                    elif s['pos'][1] >= slot['pos'][0] and s['pos'][1] <= slot[
                            'pos'][1]:
                        is_include = True
                        break
                if not is_include:
                    nlu_obj['slots'].append(slot)
                    nlu_obj['slots'] = sorted(
                        nlu_obj['slots'], key=lambda x: x['pos'][0])

        return nlu_obj

    def predict(self, sentence_result):
        """预测实体"""
        assert self.crf is not None, 'model not fitted'

        x_test = sentences_to_features(sentence_result)
        y_pred = self.crf.predict(x_test)
        # Inverse quoted string, cause Chinese
        y_pred = tuple([
            tuple([unquote(yy) for yy in y])
            for y in y_pred
        ])
        return y_pred

    @staticmethod
    def cv_eval(sentence_result,
                slot_result,
                cv=5,
                max_iterations=100,
                c1=0.17,
                c2=0.01):
        """用cv验证模型"""
        x_train = sentences_to_features(sentence_result)
        y_train = slot_result
        f1_score = make_scorer(metrics.flat_f1_score, average='weighted')

        crf = CRF(
            algorithm='lbfgs',
            c1=c1,
            c2=c2,
            max_iterations=max_iterations,
            all_possible_transitions=True,
            verbose=True)

        cv_result = cross_validate(
            crf, x_train, y_train,
            scoring=f1_score, cv=cv, verbose=10
        )

        for k, v in cv_result.items():
            logger.info(k)
            logger.info(np.mean(v))
            logger.info(v)

    def eval(self, sentence_result, slot_result):
        """绝对性的评价"""

        y_pred = self.predict(sentence_result)
        y_test = slot_result
        acc = 0
        bad = []
        for sent, real, pred in zip(sentence_result, y_test, y_pred):
            real_slot = get_slots(sent, real)
            pred_slot = get_slots(sent, pred)
            a = get_exact_right(real_slot, pred_slot)
            acc += a
            if not a:
                bad.append((sent, real, pred, real_slot, pred_slot))
        acc /= len(sentence_result)
        return acc, bad
