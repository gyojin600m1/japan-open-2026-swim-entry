#!/usr/bin/env python3
"""Regenerate the embedded search-only KANJIDIC2 reading candidates.
Usage: python3 tools/build-kana.py /path/to/kanjidic2.xml.gz
The dictionary is not an official reading of any athlete's name.
"""
import gzip
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / 'index.html'
START = '// KANJIDIC2_SEARCH_DATA_START'
END = '// KANJIDIC2_SEARCH_DATA_END'
VOICED = dict(zip('かきくけこさしすせそたちつてとはひふへほ', 'がぎぐげござじずぜぞだぢづでどばびぶべぼ'))
SEMI_VOICED = dict(zip('はひふへほ', 'ぱぴぷぺぽ'))


def normalized(text):
    text = unicodedata.normalize('NFKC', text).translate(str.maketrans({'髙': '高', '﨑': '崎'}))
    return ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in text)


def clean(reading, full=False):
    text = normalized(reading).strip('-')
    text = text.replace('.', '') if full else text.split('.')[0]
    return text.replace('ー', '') if re.fullmatch('[ぁ-ゖー]+', text) else ''


def variants(reading):
    result = {reading}
    for mapping in [VOICED, SEMI_VOICED]:
        if reading[0] in mapping:
            result.add(mapping[reading[0]] + reading[1:])
    if len(reading) > 1 and reading[-1] in 'つちくき':
        result.add(reading[:-1] + 'っ')
    return result


def main():
    source = PAGE.read_text()
    data = json.loads(re.search(r'^const DATA = (.*);$', source, re.M).group(1))
    texts = [s[1] + s[5] for s in data['sw']] + [t[1] + t[2] + t[4] for t in data['tm']]
    used = set(normalized(''.join(texts)))
    table = {}
    excluded_nanori = 0
    with gzip.open(sys.argv[1], 'rt', encoding='utf-8') as f:
        root = ET.parse(f).getroot()
    for ch in root.iter('character'):
        literal = ch.findtext('literal')
        if literal not in used:
            continue
        readings = set()
        for node in ch.iter('reading'):
            if node.get('r_type') in ['ja_on', 'ja_kun']:
                for full in [False, True]:
                    value = clean(node.text or '', full)
                    if value:
                        readings.update(variants(value))
        for node in ch.iter('nanori'):
            value = clean(node.text or '', True)
            if len(value) > 1:
                readings.update(variants(value))
            elif value:
                excluded_nanori += 1
        if readings:
            table[literal] = sorted(readings)
    header = root.find('header')
    attribution = {
        'source': 'KANJIDIC2, Electronic Dictionary Research and Development Group (EDRDG)',
        'url': 'https://www.edrdg.org/wiki/index.php/KANJIDIC_Project',
        'license': 'CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/',
        'databaseDate': header.findtext('date_of_creation') if header is not None else '',
        'changes': 'Subset for this app; kana normalization, voicing and gemination variants; one-kana nanori excluded.',
    }
    generated = START + '\n/* ' + json.dumps(attribution, ensure_ascii=False) + ' */\n'
    generated += 'const KANJI_READINGS = ' + json.dumps(table, ensure_ascii=False, separators=(',', ':')) + ';\n' + END
    if START in source:
        source = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: generated, source, flags=re.S)
    else:
        source = source.replace('/* ---------- model ---------- */', generated + '\n/* ---------- model ---------- */', 1)
    PAGE.write_text(source)
    missing = sorted(c for c in used if '\u3400' <= c <= '\u9fff' and c not in table)
    print(json.dumps({'characters': len(table), 'excludedOneKanaNanori': excluded_nanori, 'missing': missing, 'date': attribution['databaseDate']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
