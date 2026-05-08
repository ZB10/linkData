#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 LinkData.htm 中提取表格数据并转换为 CSV 格式
"""

import pandas as pd
import re
from html.parser import HTMLParser

class TableExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_row = None
        self.current_cell = ""
        self.in_cell = False
        self.table_depth = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.table_depth += 1
            if self.table_depth == 1:
                self.current_table = []
                self.current_row = None
                
        elif tag == 'tr' and self.table_depth > 0:
            self.current_row = []
            
        elif tag in ['td', 'th'] and self.table_depth > 0:
            self.in_cell = True
            self.current_cell = ""
            
    def handle_endtag(self, tag):
        if tag == 'table':
            if self.table_depth == 1 and self.current_table is not None:
                self.tables.append(self.current_table)
            self.table_depth -= 1
            
        elif tag == 'tr' and self.table_depth > 0:
            if self.current_row is not None and self.current_table is not None:
                self.current_table.append(self.current_row)
            self.current_row = None
            
        elif tag in ['td', 'th'] and self.in_cell:
            self.in_cell = False
            if self.current_row is not None:
                # 清理单元格内容
                cell_text = re.sub(r'<[^>]+>', '', self.current_cell)
                cell_text = re.sub(r'\s+', ' ', cell_text).strip()
                self.current_row.append(cell_text)
                
    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

def extract_tables_from_html(filepath):
    """从 HTML 文件中提取所有表格"""
    with open(filepath, 'r', encoding='windows-1252') as f:
        html_content = f.read()
    
    parser = TableExtractor()
    parser.feed(html_content)
    
    return parser.tables

def main():
    html_file = '/workspace/LinkData.htm'
    
    print("=" * 60)
    print("开始提取 LinkData.htm 中的表格数据...")
    print("=" * 60)
    
    # 提取所有表格
    tables = extract_tables_from_html(html_file)
    
    print(f"\n共找到 {len(tables)} 个表格")
    
    # 打印每个表格的信息
    for i, table in enumerate(tables, 1):
        print(f"\n{'='*60}")
        print(f"表格 {i}: {len(table)} 行")
        if len(table) > 0:
            print(f"列数: {len(table[0])} 列")
            print("\n前 5 行数据预览:")
            print("-" * 60)
            for j, row in enumerate(table[:5]):
                print(f"行 {j+1}: {row}")
            if len(table) > 5:
                print(f"... (还有 {len(table)-5} 行)")
    
    # 将第一个表格（通常是主要数据表）转换为 CSV
    if len(tables) > 0:
        print("\n" + "=" * 60)
        print("正在将第一个表格保存为 CSV 文件...")
        print("=" * 60)
        
        first_table = tables[0]
        
        # 检查是否有表头
        if len(first_table) > 1:
            df = pd.DataFrame(first_table[1:], columns=first_table[0])
        else:
            df = pd.DataFrame(first_table)
        
        output_csv = '/workspace/LinkData_extracted.csv'
        df.to_csv(output_csv, index=False, encoding='utf-8-sig')
        print(f"\n✓ 已成功保存至: {output_csv}")
        print(f"  数据维度: {df.shape[0]} 行 × {df.shape[1]} 列")
        print(f"\n数据预览:")
        print(df.head(10))
    
    # 如果还有其他表格，也保存它们
    if len(tables) > 1:
        print("\n" + "=" * 60)
        print("正在保存其他表格...")
        print("=" * 60)
        for i, table in enumerate(tables[1:], 2):
            if len(table) > 0:
                output_file = f'/workspace/LinkData_table_{i}.csv'
                if len(table) > 1:
                    df = pd.DataFrame(table[1:], columns=table[0])
                else:
                    df = pd.DataFrame(table)
                df.to_csv(output_file, index=False, encoding='utf-8-sig')
                print(f"✓ 表格 {i} 已保存至: {output_file} ({df.shape[0]} 行)")

if __name__ == '__main__':
    main()
