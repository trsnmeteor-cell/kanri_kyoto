import openpyxl, json, datetime
wb = openpyxl.load_workbook('sheet.xlsx', data_only=True)

# --- store master ---
s = wb['店舗']
store_by_code = {}
for r in range(7, s.max_row+1):
    code = s.cell(row=r, column=6).value
    name = s.cell(row=r, column=7).value
    area = s.cell(row=r, column=5).value
    if code is not None and name:
        try: code = int(code)
        except: pass
        store_by_code[code] = {'name': str(name), 'area': area}
print('store map size', len(store_by_code))

def tds(v):
    return int(v.total_seconds()) if isinstance(v, datetime.timedelta) else None
def hhmm(sec):
    if sec is None: return None
    h=sec//3600; m=(sec%3600)//60
    return f"{h}:{m:02d}"

# --- 超過 ---
ws = wb['超過']
chouka=[]
for r in range(11, ws.max_row+1):
    name = ws.cell(row=r, column=4).value
    if not name: continue
    code = ws.cell(row=r, column=2).value
    try: code=int(code)
    except: pass
    ov = tds(ws.cell(row=r, column=5).value)
    cnt = ws.cell(row=r, column=6).value
    fut = tds(ws.cell(row=r, column=7).value)
    chouka.append({
        'code': code,
        'store': store_by_code.get(code,{}).get('name'),
        'area': store_by_code.get(code,{}).get('area'),
        'emp': str(ws.cell(row=r, column=3).value),
        'name': str(name),
        'ovSec': ov, 'ov': hhmm(ov),
        'cnt': cnt,
        'cntNum': int(str(cnt).split('/')[0]) if cnt else 0,
        'futSec': fut, 'futH': round(fut/3600,1) if fut else None
    })
chouka.sort(key=lambda x:(-(x['ovSec'] or 0)))
print('chouka', len(chouka), 'total ov h', round(sum(x['ovSec'] or 0 for x in chouka)/3600,2))

# --- ご意見 blocks ---
g = wb['ご意見']
CATS = ['その他','飲食','料金','クレンリネス','機械','接客','-']
def parse_block(period_row, cat_row, start, end):
    p_start = g.cell(row=period_row, column=34).value
    p_end   = g.cell(row=period_row, column=36).value
    stores=[]
    for r in range(start, end+1):
        nm = g.cell(row=r, column=33).value
        if not nm: continue
        vals = [g.cell(row=r, column=c).value or 0 for c in range(34, 41)]
        vals = [int(v) if isinstance(v,(int,float)) else 0 for v in vals]
        stores.append({'name': str(nm).strip(), 'v': vals, 'total': sum(vals)})
    return {
        'start': p_start.strftime('%Y/%m/%d') if p_start else None,
        'end': p_end.strftime('%Y/%m/%d') if p_end else None,
        'label': (p_start.strftime('%Y年%-m月') if p_start else ''),
        'stores': stores,
        'catTotals': [sum(st['v'][i] for st in stores) for i in range(7)],
        'grand': sum(st['total'] for st in stores)
    }
sep = parse_block(3, 5, 6, 21)
aug = parse_block(24, 26, 27, 42)
print('SEP', sep['start'], sep['end'], 'grand', sep['grand'], 'cats', sep['catTotals'])
print('AUG', aug['start'], aug['end'], 'grand', aug['grand'], 'cats', aug['catTotals'])

out = {'cats': CATS, 'chouka': chouka, 'sep': sep, 'aug': aug,
       'generated': '2026-10-04'}
json.dump(out, open('data.json','w'), ensure_ascii=False, indent=1)
print('written data.json')
