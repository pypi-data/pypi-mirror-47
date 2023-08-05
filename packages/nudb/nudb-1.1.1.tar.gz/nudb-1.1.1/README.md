# NUDB

A Python module for NUDB.  
NUDB is a fast database and search engine.  

Menu:  

- [NUDB](#nudb)
  - [Install](#install)
  - [Usage](#usage)
    - [資料格式](#%E8%B3%87%E6%96%99%E6%A0%BC%E5%BC%8F)
    - [Connect to NUDB](#connect-to-nudb)
    - [Get DB info](#get-db-info)
    - [Search](#search)
    - [Get record by rid or key](#get-record-by-rid-or-key)
    - [Put record](#put-record)
    - [Put record from file](#put-record-from-file)
    - [Delete record by rid or key](#delete-record-by-rid-or-key)
    - [Update record](#update-record)
  - [Change log](#change-log)

## Install

```bash
$ pip install nudb
```
  
## Usage

### 資料格式

- GAIS record  
  - 以 `@` 開頭, `:` 結尾作為欄位名稱
  - `:` 之後為欄位內容
  - For example:  

    ```js
    // "@title:" 為欄位名稱
    @title:Mayday五月天 [ 頑固Tough ] Official Music Video
    ```

- JSON

### Connect to NUDB

```python
from nudb import Nudb

nudb = Nudb()
nudb.connect('host', 'port', 'db')
```

**參數說明**  
  
- host: DB host
- port: DB port
- db: 指定 DB 名稱

### Get DB info

```python
result = nudb.get_DB_info(timeout=10)
```

**參數說明**  

- timeout: 設定 timeout，單位為 s，預設是 10s.

### Search

```python
options = {
    'db': 'test',
    'matchmode': 'BestMatch',
    'groupby': '@title:',
    'getrec': 'y',
    'orderby': 'score',
    'order': 'decreasing',
    'minrid': 100,
    'maxrid': 10000,
    'ridrange': 10000,
    'minscore': 100,
    'maxscore': 5000,
    'q': '旅遊',
    'filter': '@viewcount:>1000',
    'Sensitivity': 'sensitive',
    'p': 1,
    'ps': 10,
    'select': '@title:,@body:,@viewcount:',
    'out': 'json'
}
result = nudb.search(options, timeout=10);
```

**參數說明**  

- timeout: 設定 timeout，單位為 s，預設是 10 s.
- options: query options
  - db: 指定DB
  - matchmode
    - AndMatch (預設)
    - OrMatch
    - BestMatch
  - groupby: 指定欄位群組, 預設只有輸出key, count, 欄位格式為GAIS record
  - getrec=y: 搭配groupby使用, 輸出全部資料
  - orderby
    - rid: 依照rid排序
    - score: 必須有參數q 才有score
    - groupsize: 搭配groupby
    - {FieldName}: 依照欄位(FieldName)排序
      - 在建立DB時, 數值欄位須設定 `-numfieldindex`
      - 在建立DB時, 時間欄位須設定 `-timeindex`

      ```python
      {
        'orderby': '@viewcount:'
      }
      ```

    - [min|max|ave|sum]{FieldName}: 找出欄位(FieldName)的最小/最大/平均/總和值  

      ```python
      {
        'orderby': 'sum@viewcount:' 
      }
      ```

    - order: 搭配orderby使用, 預設為decreasing
      - decreasing: 遞減
      - increasing: 遞增
    - minrid: 設定rid最小值
    - maxrid: 設定rid最大值
    - ridrange: 設定搜尋的rid範圍, rid由大至小, 僅搜尋此範圍內的資料
    - minscore: score最小值
    - maxscore: score最大值
    - q: 搜尋關鍵字
      - 可指定欄位搜尋, 欄位格式為GAIS record: 

      ```python
      {
        'q': '@title:日本旅遊'
      }
      ```

    - 可指定欄位值須完全符合:

      ```python
      {
        'q': '@id:=abcd1234'
      }
      ```

    - 可設定所有條件須符合(AndMatch):

      ```python
      {
        'q': '+@id:1234,+@name:test'
      }
      ```

      - 可搜尋多個欄位, 以","區隔:

      ```python
      {
        'q': "@title:日本旅遊,@body:東京"
      }
      ```

  - time: 可設定搜尋時間範圍
    - 在建立DB時, 時間欄位須設定 `-timeindex`
    - 限定時間區間

      ```python
      {
        'time': '=20180101-20180301'
      }
      ```

    - 特定時間以後
  
      ```python
      {
        'time': '=>20180220122000'  # YYYYMMDDHHmmss
      }
      ```

    - 特定時間以前

      ```python
      {
        'time': '=<20180220122000'  # YYYYMMDDHHmmss
      }
      ```

    - 限定某天

      ```python
      {
        'time': '=20180220'
      }
      ```

  - filter: 數值條件檢索, 沒有做數值欄位索引(-numfieldindex)也可查詢

    ```python
    {
      'filter': '@price:<200'
    }
    ```

    ```python
    {
      'filter': '@price:200-400'  # 數值區間
    }
    ```
  
  - maxcandidnum
  - Sensitivity
    - sensitive: 預設, 區分大小寫
    - insensitive: 不分大小寫
  - keytermfield
  - keytermstat
  - p: page, 指定輸出page, 預設為1
  - ps: page size, 每個page大小, 預設為10
  - select: 指定輸出欄位, 欄位格式為GAIS record, 多個欄位之間以","區隔
  - L: 指定回傳起始比數及總筆數

    ```python
    {
      'L': 30       # 回傳30筆
    }
    ```

    ```python
    {
      'L': '11,60'  # 從第11筆開始, 輸出60筆
    }
    ```

  - out: 輸出格式 (json or text)

### Get record by rid or key

```python
result = nudb.rget(data_id, search_field='rid', timeout=10)
```

**參數說明**  
  
- data_id: Record ID or primary key.
- search_field: 搜尋的欄位，rid 或 key, 預設是 rid.
- timeout: 設定 timeout，單位為 s，預設是 10s.

### Put record

```python
# format: json or text
result = nudb.rput(data, data_type, rec_beg=None, timeout=10)
```

**參數說明**  

- data: 資料
- data_type: 資料格式(json or text)
- rec_beg: record begin pattern, 若資料格式為text則必須有此參數
- timeout: 設定 timeout，單位為 s，預設是 10s.

### Put record from file

```python
result = nudb.fput(file_path, data_type, rec_beg=None, timeout=60)
```

**參數說明**  

- file_path: 要上傳的檔案
- data_type: 資料格式(json or text)
- rec_beg: record begin pattern, 若資料格式為text則必須有此參數
- timeout: 設定 timeout，單位為 s，預設是 60s.

### Delete record by rid or key

```python
result = nudb.rdel(data_id, search_field='rid', timeout=10)
```

**參數說明**  
  
- data_id: Record ID 或 primary key, 一次刪除多筆可使用`,`區隔多個 id
- search_field: 搜尋的欄位，rid 或 key, 預設是 rid.
- timeout: 設定 timeout，單位為 s，預設是 10s.

### Update record

```python
result = nudb.rupdate(data_id, data, data_type, search_field='rid', update_method='replaceRecord', timeout=10)
```

**參數說明**  

- data_id: 要更新的資料rid or primary key
- data: 更新的資料內容
- data_type: 資料格式(json or text)
- search_field: 搜尋的欄位，rid 或 key, 預設是 rid.
- update_method: 更新方式
  - replaceRecord: 取代整筆資料 (Default)
  - replaceField: 取代指定欄位的資料
- timeout: 設定 timeout，單位為 s，預設是 10s.

## [Change log](/CHANGELOG.md)
