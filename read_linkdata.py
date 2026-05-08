#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取 LinkData.htm 文件并提取表格数据
"""

from bs4 import BeautifulSoup
import pandas as pd
import os

def read_htm_tables(filepath):
    """读取 HTM 文件中的所有表格"""
    # 尝试多种编码
    encodings = ['utf-8', 'gbk', 'latin-1', 'cp1252']
    content = None
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"成功使用 {encoding} 编码读取文件")
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise Exception("无法使用任何已知编码读取文件")
    
    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.find_all('table')
    
    print(f"找到 {len(tables)} 个表格\n")
    print("=" * 80)
    
    for i, table in enumerate(tables, 1):
        print(f"\n【表格 {i}】")
        print("-" * 40)
        
        # 提取表格数据
        rows = table.find_all('tr')
        data = []
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if cols:
                row_data = [col.get_text(strip=True) for col in cols]
                data.append(row_data)
        
        if data:
            # 创建 DataFrame
            df = pd.DataFrame(data[1:], columns=data[0] if len(data) > 1 else None)
            print(df.to_string(index=False))
            print(f"行数: {len(df)}, 列数: {len(df.columns)}")
        else:
            print("空表格")
        
        print("=" * 80)
    
    return tables

if __name__ == "__main__":
    filepath = "LinkData.htm"
    
    if not os.path.exists(filepath):
        print(f"错误: 文件 {filepath} 不存在!")
        exit(1)
    
    print(f"开始读取 {filepath} ...")
    tables = read_htm_tables(filepath)
    print(f"\n完成! 共解析 {len(tables)} 个表格")
