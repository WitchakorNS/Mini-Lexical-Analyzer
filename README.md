# Mini-Lexical-Analyzer
ProLang Hod Hod

โปรเจกต์ Mini Lexical Analyzer ด้วย Python และ SLY สำหรับวิชา Programming Languages Concepts and Paradigms

ดูหน้าที่ โค้ด รายงาน และการทดสอบของสมาชิกใน [การแบ่งงาน](TEAM_ASSIGNMENTS.md)

## ติดตั้งและรันโปรแกรม

ผู้รับผิดชอบ: **เตย** — ใช้ Python 3.9 ขึ้นไป เปิด Terminal ที่รากโปรเจกต์

```bash
python -m venv .venv
```

เปิด environment บน Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

หรือบน Linux / WSL / macOS:

```bash
source .venv/bin/activate
```

จากนั้นติดตั้งและรัน:

```bash
python -m pip install -r requirements.txt
python main.py inputs/sample1.txt
python main.py inputs/sample2.txt
python main.py inputs/all_tokens.txt
python main.py inputs/lexical_error.txt
python -m pytest -q
```

ใช้ `python3` แทน `python` ได้ตามเครื่อง รับไฟล์ `.txt` แบบ UTF-8 หรือ UTF-8 BOM
ถ้า path มีช่องว่าง ให้ครอบด้วย double quote เช่น `python main.py "inputs/my input.txt"`
โปรแกรมคืน exit code `0` เมื่อสำเร็จ, `1` เมื่อพบ lexical error, `2` เมื่อ argument หรือไฟล์มีปัญหา

`sample1.txt` และ `sample2.txt` ตรงกับตัวอย่างใน PDF; `all_tokens.txt` เพิ่มตัวอย่างให้ครบทุก token
ส่วน `lexical_error.txt` ต้องแสดงเพียง:

```text
new identifier: A
Lexical error: unexpected character @
```

การรันแต่ละครั้งเริ่ม Symbol Table ใหม่ และเก็บเฉพาะ Identifier โดยแยกตัวพิมพ์เล็ก/ใหญ่
String เก็บ quote และข้อความเดิม ไม่แปล escape sequence; ไม่รองรับทศนิยมหรือ String หลายบรรทัด
Comment จบที่ `*/` แรกและไม่รองรับ nested comment
ข้อตกลงเพิ่มเติม: `1score` เป็น lexical error ที่ `1`; String/Block Comment ที่ไม่ปิดเป็น error ที่อักขระเปิด
ข้อความ error คงรูปแบบโจทย์ ส่วนเหตุผลและตำแหน่งเก็บไว้ใน `LexicalError` สำหรับตรวจสอบในโค้ด

## โครงสร้างและเจ้าของโค้ด

| ไฟล์ / ส่วน | ผู้รับผิดชอบตามแผน |
|---|---|
| `src/lexer.py` — Operators, Parentheses, Semicolon | ปาม |
| `src/lexer.py` — Keywords, Identifier | แฟนต้า |
| `src/lexer.py` — Integer, String | โรมัน |
| `src/lexer.py` — Comments, Whitespace, Lexical Error | หยก |
| `src/symbol_table.py`, `src/output_formatter.py` | พอต |
| `main.py`, `src/__init__.py`, dependencies, `inputs/` และการรวม | เตย |
| `test/test_lexer.py` | ทุกคนตาม comment และ prefix ของ test; เตยรวม |

คอมเมนต์ภาษาไทยในแต่ละส่วนอธิบายกฎ เหตุผล และเจ้าของตามแผนแบ่งงาน
ดูรายละเอียด Regex, DFA และผลทดสอบใน [รายงาน](docs/report.md)
และดูวิธีประกาศกฎเพิ่มเติมจาก [เอกสาร SLY](https://sly.readthedocs.io/en/latest/sly.html)

## Branch ของสมาชิก

| สมาชิก | Branch | คำสั่งเข้า Branch ครั้งแรกหลัง Clone |
|---|---|---|
| ปาม | `Palm` | `git switch --track origin/Palm` |
| แฟนต้า | `Fanta` | `git switch --track origin/Fanta` |
| โรมัน | `Roman` | `git switch --track origin/Roman` |
| หยก | `ํYok` | `git switch --track origin/ํYok` |
| พอต | `Port` | `git switch --track origin/Port` |
| เตย | `Toey` | `git switch --track origin/Toey` |
| งานรวม | `main` | ใช้รับงานจาก Pull Request ที่ตรวจแล้ว |

ชื่อ Branch ต้องตรงทั้งตัวพิมพ์เล็กและใหญ่ โดยชื่อ `ํYok` ปัจจุบันมีอักขระไทย `ํ` (U+0E4D) นำหน้า `Y` ให้คัดลอกทั้งชื่อ หากกลุ่มเปลี่ยนชื่อ Branch ภายหลัง ให้แก้ตารางและคำสั่งตามชื่อใหม่

## 1. เตรียมโปรเจกต์ครั้งแรก

ติดตั้ง Git และลงชื่อเข้าใช้ GitHub ให้พร้อม จากนั้นเปิด Terminal ในโฟลเดอร์ที่จะเก็บโปรเจกต์

คัดลอก URL จากปุ่ม **Code** บน GitHub แล้วแทนที่ `<REPOSITORY_URL>` ทั้งก้อนในคำสั่งนี้ด้วย URL จริง:

```bash
git clone <REPOSITORY_URL>
cd Mini-Lexical-Analyzer
git fetch origin
git branch -a
```

ถ้ามีโปรเจกต์อยู่แล้ว ให้เปิด Terminal ในโฟลเดอร์ `Mini-Lexical-Analyzer` แล้วเริ่มจาก `git fetch origin` ได้เลย

ตั้งชื่อและอีเมลสำหรับ Commit ใน Repository นี้ โดยเปลี่ยนเป็นข้อมูลของตัวเอง:

```bash
git config user.name "ชื่อของตัวเอง"
git config user.email "อีเมล GitHub หรืออีเมล noreply ของตัวเอง"
```

## 2. เข้า Branch ของตัวเองและดึงงานล่าสุด

ตัวอย่างต่อไปนี้ใช้ **แฟนต้า / `Fanta`** สมาชิกคนอื่นเปลี่ยนชื่อ Branch เป็นของตัวเองตามตาราง

ตรวจงานค้างก่อนเปลี่ยน Branch:

```bash
git status
```

ถ้ามีไฟล์แก้ค้างอยู่ ให้ตรวจว่าเป็นงานของ Branch ใดและจัดเก็บให้เรียบร้อยก่อนเปลี่ยน Branch เพื่อไม่ให้งานปะปนกัน

ถ้ายังไม่มี Branch `Fanta` บนเครื่อง ให้ใช้คำสั่งนี้ครั้งเดียว:

```bash
git switch --track origin/Fanta
```

ถ้ามี Branch บนเครื่องแล้ว ให้ใช้:

```bash
git switch Fanta
```

จากนั้นดึงงานล่าสุดของ Branch ตัวเอง และรวมการเปลี่ยนแปลงล่าสุดจาก `main` ก่อนเริ่มเขียนงาน:

```bash
git fetch origin
git pull --ff-only
git merge origin/main
git branch --show-current
```

คำสั่งสุดท้ายต้องแสดงชื่อ Branch ของตัวเอง หาก Merge เกิด Conflict ให้ทำตามหัวข้อแก้ Conflict ด้านล่างก่อนเริ่มงานต่อ

## 3. แก้ไฟล์และ Commit งาน

ทำงานตามส่วนที่รับผิดชอบใน [TEAM_ASSIGNMENTS.md](TEAM_ASSIGNMENTS.md) แล้วรัน Test ที่เกี่ยวข้องเมื่อมีโค้ดและ Test พร้อมใช้งาน

ตรวจไฟล์ที่เปลี่ยนและรายละเอียดก่อนเตรียม Commit:

```bash
git status
git diff
```

เลือก `git add` เฉพาะไฟล์ที่ต้องการส่ง ตัวอย่างไฟล์ของแฟนต้า:

```bash
git add src/lexer.py docs/automata/identifier.mmd docs/report.md test/test_lexer.py
git diff --cached
git commit -m "Add keyword and identifier rules with tests"
```

ชื่อไฟล์และข้อความ Commit เป็นตัวอย่าง ให้ปรับตามงานที่ทำจริง `git diff --cached` ใช้ตรวจเนื้อหาที่จะเข้า Commit โดยเฉพาะไฟล์ที่หลายคนแก้ร่วมกัน

## 4. Push ขึ้น GitHub

สำหรับ Branch `Fanta` ใช้:

```bash
git push -u origin Fanta
```

สมาชิกคนอื่นเปลี่ยน `Fanta` เป็นชื่อ Branch ตัวเอง คำสั่งนี้อัป Commit ขึ้น Branch ที่ระบุและตั้งค่าการติดตาม Branch นั้นไว้

หลังตั้งค่าแล้ว การอัปงานครั้งต่อไปจาก Branch เดิมใช้ `git push` ได้:

```bash
git push
```

ไฟล์ที่แก้แต่ยังไม่ได้ Commit จะยังไม่ถูกอัปขึ้น GitHub

## 5. เปิด Pull Request เพื่อรวมเข้า main

1. เปิด Repository บน GitHub แล้วเข้าแท็บ **Pull requests** → **New pull request**
2. เลือก **base: `main`** และ **compare: Branch ของตัวเอง** เช่น `Fanta`
3. ตรวจรายการไฟล์และสิ่งที่เปลี่ยนให้ตรงกับงานที่จะส่ง
4. ตั้งชื่อและเขียนรายละเอียดสั้น ๆ ว่าทำอะไร เปลี่ยนไฟล์ไหน และทดสอบอย่างไร
5. กด **Create pull request** แล้วแจ้งเตยหรือคนที่กลุ่มมอบหมายให้ตรวจและรวมงาน
6. หากต้องแก้เพิ่ม ให้ Commit และ Push บน Branch เดิม Pull Request ที่ยังเปิดอยู่จะอัปเดตตาม

ถ้ายังไม่ได้รัน Test ให้ระบุไว้ใน Pull Request ตามจริง เมื่อรวมงานแล้ว สมาชิกทุกคนควรดึง `main` มารวมใน Branch ของตัวเองก่อนเริ่มงานรอบใหม่

## 6. ทำงานรอบต่อไป

เริ่มรอบใหม่โดยตรวจว่างานรอบก่อน Commit เรียบร้อยแล้ว จากนั้นใช้ขั้นตอนเดิม ตัวอย่างของแฟนต้า:

```bash
git switch Fanta
git fetch origin
git pull --ff-only
git merge origin/main
```

แก้ไฟล์ → ทดสอบ → `git add` ไฟล์ที่ต้องการ → `git commit` → `git push` → เปิด Pull Request เมื่อพร้อมรวมงาน

## การแก้ Merge Conflict

ไฟล์อย่าง `src/lexer.py`, `docs/report.md` และ `test/test_lexer.py` มีหลายคนรับผิดชอบร่วมกัน หาก Git รวมการเปลี่ยนแปลงอัตโนมัติไม่ได้ ให้ทำดังนี้:

1. ใช้ `git status` ดูว่าไฟล์ใด Conflict
2. เปิดไฟล์นั้น หาบริเวณที่มี `<<<<<<<`, `=======`, `>>>>>>>`
3. ประสานเจ้าของโค้ด แล้วแก้ให้เก็บงานที่จำเป็นของทั้งสองฝั่ง ลบเครื่องหมาย Conflict ออกให้หมด
4. รัน Test ที่เกี่ยวข้องกับส่วนที่แก้
5. ใช้ `git add` ระบุไฟล์ที่แก้ครบแล้ว จากนั้น Commit เพื่อจบ Merge

ตัวอย่างกรณี Conflict เฉพาะ `src/lexer.py`:

```bash
git add src/lexer.py
git commit -m "Merge main and resolve lexer conflicts"
git push
```

ถ้ายังมีไฟล์อื่น Conflict ต้องแก้และ `git add` ไฟล์เหล่านั้นก่อน Commit ด้วย

## ปัญหาที่อาจพบ

| ปัญหา | วิธีจัดการ |
|---|---|
| `git switch --track` แจ้งว่า Branch มีอยู่แล้ว | ใช้ `git switch ชื่อBranch` เพื่อเข้า Branch บนเครื่องที่มีอยู่แล้ว |
| หา Branch ไม่เจอ | ใช้ `git fetch origin` แล้ว `git branch -a` ตรวจชื่อจริง โดยเฉพาะตัวพิมพ์ใหญ่และชื่อ `ํYok` |
| Push ถูกปฏิเสธเพราะ Branch บน GitHub มี Commit เพิ่ม | Commit งานบนเครื่องให้เรียบร้อย แล้วใช้ `git fetch origin` และ `git merge origin/Fanta` โดยเปลี่ยนชื่อให้ตรง Branch ตัวเอง แก้ Conflict ถ้ามี จากนั้น Push อีกครั้ง |
| `git pull --ff-only` แจ้งว่าประวัติแยกจากกัน | หลังจัดเก็บงานค้างแล้ว ใช้ `git fetch origin` และ `git merge origin/Fanta` โดยเปลี่ยนชื่อเป็น Branch ตัวเอง เพื่อรวมประวัติก่อนทำงานต่อ |
| Push ไม่ผ่านเพราะสิทธิ์ | ตรวจว่าลงชื่อเข้า GitHub ด้วยบัญชีที่มีสิทธิ์เขียน Repository และรับคำเชิญเข้าร่วมแล้ว |
| ไม่แน่ใจว่ากำลังอยู่ Branch ไหน | ใช้ `git branch --show-current` ก่อน Commit และ Push |

ให้แก้ปัญหาการรวมงานด้วยการตรวจ Commit และ Merge ร่วมกัน หลีกเลี่ยง `git push --force` เพราะอาจเขียนทับงานบน Branch ของเพื่อน
