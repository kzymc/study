#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从PDF第16页（第一章）开始提取文本，按一级标题（卷）和二级标题（章）组织成Markdown。
v3 - 修复康熙部首字符问题，先归一化再识别标题
"""

import re
import unicodedata
from pypdf import PdfReader

PDF_PATH = r'c:\Users\A\.trae-cn\attachments\6ab35575ee59b2f665d713af\190ee1b2-7bdd-4d87-92d9-e2c015b18592_381c2d2b-74e2-4e21-b2fc-4e3476f5fc59_乌合之众：大众心理研究（畅销125年纪念版）.pdf'
OUTPUT_PATH = r'd:\trce\6ab35575ee59b2f665d713ac\乌合之众_第一卷起.md'
START_PAGE = 15  # 第16页对应索引15（0-based）


# 康熙部首 (U+2F00-U+2FD5) 到 CJK 统一汉字的映射表
# 共214个部首，映射到对应的常用汉字
KANGXI_RADICAL_MAP = {
    '\u2F00': '一', '\u2F01': '丨', '\u2F02': '丶', '\u2F03': '丿',
    '\u2F04': '乙', '\u2F05': '亅', '\u2F06': '二', '\u2F07': '亠',
    '\u2F08': '人', '\u2F09': '儿', '\u2F0A': '入', '\u2F0B': '八',
    '\u2F0C': '冂', '\u2F0D': '冖', '\u2F0E': '冫', '\u2F0F': '几',
    '\u2F10': '凵', '\u2F11': '刀', '\u2F12': '力', '\u2F13': '勹',
    '\u2F14': '匕', '\u2F15': '匚', '\u2F16': '匸', '\u2F17': '十',
    '\u2F18': '卜', '\u2F19': '卩', '\u2F1A': '厂', '\u2F1B': '厶',
    '\u2F1C': '又', '\u2F1D': '口', '\u2F1E': '囗', '\u2F1F': '土',
    '\u2F20': '士', '\u2F21': '夂', '\u2F22': '夊', '\u2F23': '夕',
    '\u2F24': '大', '\u2F25': '女', '\u2F26': '子', '\u2F27': '宀',
    '\u2F28': '寸', '\u2F29': '小', '\u2F2A': '尢', '\u2F2B': '尸',
    '\u2F2C': '屮', '\u2F2D': '山', '\u2F2E': '川', '\u2F2F': '工',
    '\u2F30': '己', '\u2F31': '巾', '\u2F32': '干', '\u2F33': '幺',
    '\u2F34': '广', '\u2F35': '廴', '\u2F36': '廾', '\u2F37': '弋',
    '\u2F38': '弓', '\u2F39': '彐', '\u2F3A': '彡', '\u2F3B': '彳',
    '\u2F3C': '心', '\u2F3D': '戈', '\u2F3E': '户', '\u2F3F': '手',
    '\u2F40': '支', '\u2F41': '攵', '\u2F42': '文', '\u2F43': '斗',
    '\u2F44': '斤', '\u2F45': '方', '\u2F46': '无', '\u2F47': '日',
    '\u2F48': '曰', '\u2F49': '月', '\u2F4A': '木', '\u2F4B': '欠',
    '\u2F4C': '止', '\u2F4D': '歹', '\u2F4E': '殳', '\u2F4F': '毋',
    '\u2F50': '比', '\u2F51': '毛', '\u2F52': '氏', '\u2F53': '气',
    '\u2F54': '水', '\u2F55': '火', '\u2F56': '爪', '\u2F57': '父',
    '\u2F58': '爻', '\u2F59': '爿', '\u2F5A': '片', '\u2F5B': '牙',
    '\u2F5C': '牛', '\u2F5D': '犬', '\u2F5E': '玄', '\u2F5F': '玉',
    '\u2F60': '瓜', '\u2F61': '瓦', '\u2F62': '甘', '\u2F63': '生',
    '\u2F64': '用', '\u2F65': '田', '\u2F66': '疋', '\u2F67': '疒',
    '\u2F68': '癶', '\u2F69': '白', '\u2F6A': '皮', '\u2F6B': '皿',
    '\u2F6C': '目', '\u2F6D': '矛', '\u2F6E': '矢', '\u2F6F': '石',
    '\u2F70': '示', '\u2F71': '禸', '\u2F72': '禾', '\u2F73': '穴',
    '\u2F74': '立', '\u2F75': '竹', '\u2F76': '米', '\u2F77': '糸',
    '\u2F78': '缶', '\u2F79': '网', '\u2F7A': '羊', '\u2F7B': '羽',
    '\u2F7C': '老', '\u2F7D': '而', '\u2F7E': '耒', '\u2F7F': '耳',
    '\u2F80': '聿', '\u2F81': '肉', '\u2F82': '臣', '\u2F83': '自',
    '\u2F84': '至', '\u2F85': '臼', '\u2F86': '舌', '\u2F87': '舛',
    '\u2F88': '舟', '\u2F89': '艮', '\u2F8A': '色', '\u2F8B': '艸',
    '\u2F8C': '虍', '\u2F8D': '虫', '\u2F8E': '血', '\u2F8F': '行',
    '\u2F90': '衣', '\u2F91': '襾', '\u2F92': '見', '\u2F93': '角',
    '\u2F94': '言', '\u2F95': '谷', '\u2F96': '豆', '\u2F97': '豕',
    '\u2F98': '豸', '\u2F99': '貝', '\u2F9A': '赤', '\u2F9B': '走',
    '\u2F9C': '足', '\u2F9D': '身', '\u2F9E': '車', '\u2F9F': '辛',
    '\u2FA0': '辰', '\u2FA1': '辵', '\u2FA2': '邑', '\u2FA3': '酉',
    '\u2FA4': '釆', '\u2FA5': '里', '\u2FA6': '金', '\u2FA7': '長',
    '\u2FA8': '門', '\u2FA9': '阜', '\u2FAA': '隶', '\u2FAB': '隹',
    '\u2FAC': '雨', '\u2FAD': '靑', '\u2FAE': '非', '\u2FAF': '面',
    '\u2FB0': '革', '\u2FB1': '韋', '\u2FB2': '韭', '\u2FB3': '音',
    '\u2FB4': '頁', '\u2FB5': '風', '\u2FB6': '飛', '\u2FB7': '食',
    '\u2FB8': '首', '\u2FB9': '香', '\u2FBA': '馬', '\u2FBB': '骨',
    '\u2FBC': '高', '\u2FBD': '髟', '\u2FBE': '鬥', '\u2FBF': '鬯',
    '\u2FC0': '鬲', '\u2FC1': '鬼', '\u2FC2': '魚', '\u2FC3': '鳥',
    '\u2FC4': '鹿', '\u2FC5': '麥', '\u2FC6': '麻', '\u2FC7': '黃',
    '\u2FC8': '黍', '\u2FC9': '黑', '\u2FCA': '黹', '\u2FCB': '黽',
    '\u2FCC': '鼎', '\u2FCD': '鼓', '\u2FCE': '鼠', '\u2FCF': '鼻',
    '\u2FD0': '齊', '\u2FD1': '齒', '\u2FD2': '龍', '\u2FD3': '龜',
    '\u2FD4': '龠', '\u2FD5': '丿',
}

# CJK部首补充 (U+2E80-U+2EFF) 到普通汉字的映射
# 这些是部首的变体形式，映射到对应的CJK统一汉字
CJK_RADICAL_SUPPLEMENT_MAP = {
    '\u2E80': '一', '\u2E81': '丨', '\u2E82': '丶', '\u2E83': '丿',
    '\u2E84': '乙', '\u2E85': '亅', '\u2E86': '二', '\u2E87': '亠',
    '\u2E88': '人', '\u2E89': '儿', '\u2E8A': '入', '\u2E8B': '八',
    '\u2E8C': '冂', '\u2E8D': '冖', '\u2E8E': '冫', '\u2E8F': '几',
    '\u2E90': '凵', '\u2E91': '刀', '\u2E92': '力', '\u2E93': '勹',
    '\u2E94': '匕', '\u2E95': '匚', '\u2E96': '匸', '\u2E97': '十',
    '\u2E98': '卜', '\u2E99': '卩', '\u2E9A': '厂', '\u2E9B': '厶',
    '\u2E9C': '又', '\u2E9D': '口', '\u2E9E': '囗', '\u2E9F': '土',
    '\u2EA0': '民', '\u2EA1': '夂', '\u2EA2': '夊', '\u2EA3': '夕',
    '\u2EA4': '大', '\u2EA5': '女', '\u2EA6': '子', '\u2EA7': '宀',
    '\u2EA8': '寸', '\u2EA9': '小', '\u2EAA': '尢', '\u2EAB': '尸',
    '\u2EAC': '屮', '\u2EAD': '山', '\u2EAE': '川', '\u2EAF': '工',
    '\u2EB0': '己', '\u2EB1': '巾', '\u2EB2': '干', '\u2EB3': '幺',
    '\u2EB4': '广', '\u2EB5': '廴', '\u2EB6': '廾', '\u2EB7': '弋',
    '\u2EB8': '弓', '\u2EB9': '彐', '\u2EBA': '彡', '\u2EBB': '彳',
    '\u2EBC': '心', '\u2EBD': '戈', '\u2EBE': '户', '\u2EBF': '手',
    '\u2EC0': '支', '\u2EC1': '攵', '\u2EC2': '文', '\u2EC3': '斗',
    '\u2EC4': '斤', '\u2EC5': '见', '\u2EC6': '角', '\u2EC7': '日',
    '\u2EC8': '曰', '\u2EC9': '月', '\u2ECA': '木', '\u2ECB': '欠',
    '\u2ECC': '止', '\u2ECD': '歹', '\u2ECE': '殳', '\u2ECF': '毋',
    '\u2ED0': '比', '\u2ED1': '毛', '\u2ED2': '氏', '\u2ED3': '气',
    '\u2ED4': '水', '\u2ED5': '火', '\u2ED6': '爪', '\u2ED7': '父',
    '\u2ED8': '爻', '\u2ED9': '爿', '\u2EDA': '片', '\u2EDB': '牙',
    '\u2EDC': '牛', '\u2EDD': '犬', '\u2EDE': '玄', '\u2EDF': '玉',
    '\u2EE0': '瓜', '\u2EE1': '瓦', '\u2EE2': '甘', '\u2EE3': '生',
    '\u2EE4': '用', '\u2EE5': '田', '\u2EE6': '疋', '\u2EE7': '疒',
    '\u2EE8': '癶', '\u2EE9': '白', '\u2EEA': '皮', '\u2EEB': '皿',
    '\u2EEC': '目', '\u2EED': '矛', '\u2EEE': '矢', '\u2EEF': '石',
    '\u2EF0': '示', '\u2EF1': '禸', '\u2EF2': '禾', '\u2EF3': '穴',
    '\u2EF4': '立', '\u2EF5': '竹', '\u2EF6': '米', '\u2EF7': '糸',
    '\u2EF8': '缶', '\u2EF9': '网', '\u2EFA': '羊', '\u2EFB': '羽',
    '\u2EFC': '老', '\u2EFD': '而', '\u2EFE': '耒', '\u2EFF': '耳',
}


def normalize_radicals(text):
    """将康熙部首和CJK部首补充字符转换为普通汉字"""
    result = []
    for ch in text:
        if ch in KANGXI_RADICAL_MAP:
            result.append(KANGXI_RADICAL_MAP[ch])
        elif ch in CJK_RADICAL_SUPPLEMENT_MAP:
            # CJK部首补充中很多也是部首形式，尽量映射
            result.append(CJK_RADICAL_SUPPLEMENT_MAP[ch])
        else:
            result.append(ch)
    return ''.join(result)


def clean_text(text):
    """全面清理文本"""
    # 去除空字节
    text = text.replace('\x00', '')
    # 去除 (cid:xxx) 类乱码
    text = re.sub(r'\(cid:\d+\)', '', text)
    # 归一化部首字符
    text = normalize_radicals(text)
    return text


def extract_all_text(reader, start_page):
    """从指定页开始提取所有文本，逐页提取并清理"""
    all_text = ''
    for i in range(start_page, len(reader.pages)):
        text = reader.pages[i].extract_text()
        if text:
            text = clean_text(text)
            all_text += text + '\n'
    return all_text


def split_by_headings(text):
    """
    用正则表达式找出所有卷和章的标题，将文本分割成结构化的块。
    返回列表：[(heading_level, heading_text, content), ...]
    """
    headings = []
    
    # 匹配卷标题: 第X卷 + 卷名（卷名到换行或到"第X章"之前）
    vol_pattern = re.compile(r'^(第[一二三四五六七八九十百]+卷)\s*(.*?)$', re.MULTILINE)
    for m in vol_pattern.finditer(text):
        vol_num = m.group(1)
        vol_name = m.group(2).strip()
        headings.append((m.start(), 1, vol_num, vol_name))
    
    # 匹配章标题: 第X章 + 章名
    chap_pattern = re.compile(r'^(第[一二三四五六七八九十百]+章)\s+(.+)$', re.MULTILINE)
    for m in chap_pattern.finditer(text):
        chap_num = m.group(1)
        chap_name = m.group(2).strip()
        headings.append((m.start(), 2, chap_num, chap_name))
    
    # 按位置排序
    headings.sort(key=lambda x: x[0])
    
    # 过滤掉在"提要："行中的误匹配（如"提要：...第X章..."）
    filtered = []
    for pos, level, num, name in headings:
        # 检查前面是否有"提要："且在同一行附近
        line_start = text.rfind('\n', 0, pos) + 1
        line_text = text[line_start:pos + len(num) + len(name) + 10]
        if '提要' in line_text and line_text.index('提要') < pos - line_start:
            continue  # 这是提要中的引用，不是真正的标题
        filtered.append((pos, level, num, name))
    
    headings = filtered
    
    # 根据标题位置分割文本
    blocks = []
    for i, (pos, level, num, name) in enumerate(headings):
        # 确定该标题的结束位置（下一个标题的开始位置）
        if i + 1 < len(headings):
            end_pos = headings[i+1][0]
        else:
            end_pos = len(text)
        
        # 提取标题行之后的内容
        heading_line_end = text.find('\n', pos)
        if heading_line_end == -1 or heading_line_end > end_pos:
            heading_line_end = end_pos
        
        # 如果卷/章名在下一行（当前行名称为空），需要多取一行
        if not name:
            next_line_end = text.find('\n', heading_line_end + 1)
            if next_line_end != -1 and next_line_end < end_pos:
                next_line = text[heading_line_end+1:next_line_end].strip()
                # 检查下一行是不是另一个标题开头
                if not re.match(r'^第[一二三四五六七八九十百]+[卷章]', next_line):
                    name = next_line
                    heading_line_end = next_line_end
        
        # 处理名称和标题在同一行但卷名之后还有内容的情况
        # 确保content_start在标题行之后
        content_start = heading_line_end + 1
        # 如果content_start处的行就是name（重复），再跳过一行
        next_content_line_end = text.find('\n', content_start)
        if next_content_line_end != -1 and next_content_line_end < end_pos:
            next_line_text = text[content_start:next_content_line_end].strip()
            if next_line_text == name:
                content_start = next_content_line_end + 1
        content = text[content_start:end_pos].strip()
        
        full_title = f'{num} {name}'.strip()
        blocks.append((level, full_title, content))
    
    return blocks


def clean_content(content):
    """清理正文内容：合并段落、去除页眉页脚等"""
    lines = content.split('\n')
    paragraphs = []
    current_para = ''
    
    for line in lines:
        stripped = line.strip()
        
        # 空行表示段落分隔
        if not stripped:
            if current_para:
                paragraphs.append(current_para)
                current_para = ''
            continue
        
        # 跳过纯数字行（页码）
        if re.match(r'^\d+$', stripped):
            continue
        
        # 跳过过短的、不含标点的行（可能是页眉碎片）
        if len(stripped) < 5 and not re.search(r'[。，、；：！？]', stripped):
            continue
        
        # 判断当前行是否是段落结尾
        is_end = re.search(r'[。！？…」』）】》"\']\s*$', stripped)
        
        if current_para:
            current_para += stripped
        else:
            current_para = stripped
        
        if is_end:
            paragraphs.append(current_para)
            current_para = ''
    
    if current_para:
        paragraphs.append(current_para)
    
    return '\n\n'.join(paragraphs)


def build_markdown(blocks):
    """根据结构化块构建Markdown文本"""
    md_parts = []
    
    for level, title, content in blocks:
        if level == 1:
            md_parts.append(f'# {title}')
        elif level == 2:
            md_parts.append(f'## {title}')
        md_parts.append('')
        
        cleaned = clean_content(content)
        if cleaned:
            md_parts.append(cleaned)
            md_parts.append('')
    
    return '\n'.join(md_parts)


def main():
    print('正在读取PDF...')
    reader = PdfReader(PDF_PATH)
    print(f'PDF总页数: {len(reader.pages)}')
    print(f'从第{START_PAGE+1}页开始提取...')
    
    # 提取全部文本（含部首归一化）
    full_text = extract_all_text(reader, START_PAGE)
    print(f'提取文本总字符数: {len(full_text)}')
    
    # 按标题分割
    blocks = split_by_headings(full_text)
    print(f'识别到 {len(blocks)} 个标题块')
    
    # 打印结构概览
    print('\n===== 结构概览 =====')
    for level, title, content in blocks:
        prefix = '#' * level
        print(f'{prefix} {title}  (内容约{len(content)}字)')
    
    # 构建Markdown
    md_text = build_markdown(blocks)
    
    # 保存
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(md_text)
    
    print(f'\n已保存到: {OUTPUT_PATH}')
    print(f'总字符数: {len(md_text)}')


if __name__ == '__main__':
    main()
