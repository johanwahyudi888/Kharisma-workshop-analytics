# -*- coding: utf-8 -*-
"""Komponen tampilan + perhitungan murni (tanpa Streamlit) untuk halaman referensi V17.
Semua fungsi menerima/mengembalikan pandas / string HTML sehingga bisa diuji tanpa menjalankan aplikasi."""
import re
import calendar
import html as _h
import numpy as np
import pandas as pd

DAY_ID = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
MONTH_ID = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
MON_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']


def esc(x):
    return _h.escape(str(x))


def fmt_rp(x):
    try:
        return 'Rp ' + f'{float(x):,.0f}'.replace(',', '.')
    except Exception:
        return 'Rp 0'


def fmt_jt(x):
    try:
        return f'Rp {float(x) / 1e6:,.1f} Jt'
    except Exception:
        return 'Rp 0.0 Jt'


def fmt_num(x):
    try:
        return f'{int(round(float(x))):,}'.replace(',', '.')
    except Exception:
        return '0'


def pct_tone(pct):
    """>=100 hijau, >=90 biru, >=70 oranye, selain itu merah."""
    if pct >= 100: return 'green'
    if pct >= 90: return 'blue'
    if pct >= 70: return 'orange'
    return 'red'


def status_label(pct):
    if pct >= 100: return 'Tercapai', 'green'
    if pct >= 80: return 'Mendekati', 'blue'
    return 'Perlu Ditingkatkan', 'red'


def growth_pct(new, old):
    try:
        old = float(old); new = float(new)
    except Exception:
        return None
    if old == 0:
        return None
    return (new / old - 1.0) * 100.0


def fmt_growth(g):
    if g is None or (isinstance(g, float) and (np.isnan(g) or np.isinf(g))):
        return '-'
    return f'{g:+.1f}%'


# ------------------------------------------------------------------ HTML komponen
def head_card(title, subtitle_html='', icon='insights', tone='blue'):
    return (f'<div class="rk-head"><span class="rk-hic {tone}"><span class="msr">{icon}</span></span>'
            f'<div><b>{esc(title)}</b><small>{subtitle_html}</small></div></div>')


def dark_banner(html_inner, tag='', big=False):
    t = f'<span class="rk-tag">{esc(tag)}</span>' if tag else ''
    return f'<div class="rk-dark{" big" if big else ""}"><span class="rk-dot"></span><div class="rk-dark-t">{html_inner}</div>{t}</div>'


def kpi_card(label, value, sub='', icon='', tone='blue', badge=''):
    ic = f'<span class="rk-ic {tone}"><span class="msr">{icon}</span></span>' if icon else ''
    bd = f'<span class="rk-badge {tone}">{esc(badge)}</span>' if badge else ''
    sb = f'<div class="rk-foot">{sub}</div>' if sub else ''
    return (f'<div class="rk-card"><div class="rk-top"><span class="rk-lab">{esc(label)}</span>{ic}</div>'
            f'<div class="rk-val">{value}</div>{("<div class=rk-row>" + bd + "</div>") if bd else ""}{sb}</div>')


def progress_card(label, actual_txt, target_txt, pct, icon, foot_left='', foot_right='', target_set=True):
    tone = pct_tone(pct) if target_set else 'gray'
    width = max(0.0, min(pct, 100.0)) if target_set else 0.0
    badge = f'{pct:.1f}%' if target_set else 'target belum diisi'
    return (f'<div class="rk-card"><div class="rk-top"><span class="rk-lab">{esc(label)}</span>'
            f'<span class="rk-ic {tone}"><span class="msr">{icon}</span></span></div>'
            f'<div class="rk-val">{actual_txt} <small>/ {target_txt}</small></div>'
            f'<div class="rk-row"><span>Pencapaian:</span><b class="rk-badge {tone}">{badge}</b></div>'
            f'<div class="rk-bar"><i class="{tone}" style="width:{width:.1f}%"></i></div>'
            f'<div class="rk-foot2"><span>{foot_left}</span><span>{foot_right}</span></div></div>')


def mini_card(label, value, sub='', tone='plain'):
    return (f'<div class="rk-mini {tone}"><span class="rk-lab">{esc(label)}</span>'
            f'<div class="rk-mval">{value}</div><small>{sub}</small></div>')


def grid(cards, min_w=190, cls=''):
    return f'<div class="rk-grid {cls}" style="--rkw:{min_w}px">' + ''.join(cards) + '</div>'


def insight_band(title, items):
    """items: list of (judul_kecil, teks_html, tone)"""
    cells = ''.join(f'<div class="rk-ins {t}"><b>{esc(h)}</b><p>{txt}</p></div>' for h, txt, t in items)
    return f'<div class="rk-band"><div class="rk-band-t"><span class="msr">auto_awesome</span>{esc(title)}</div><div class="rk-band-g">{cells}</div></div>'


def status_badge(label, tone):
    return f'<span class="rk-badge {tone}">{esc(label)}</span>'


def table_html(headers, rows, num_cols=(), bold_last=False, hl_cols=None, row_cls=None):
    """headers: list[str]; rows: list[list[str-html]]; num_cols: indeks kolom rata kanan."""
    hl_cols = hl_cols or {}
    th = ''.join(f'<th class="{"n" if i in num_cols else ""} {hl_cols.get(i, "")}">{esc(h)}</th>' for i, h in enumerate(headers))
    body = ''
    for ri, r in enumerate(rows):
        last = bold_last and ri == len(rows) - 1
        rc_ = (row_cls[ri] if row_cls and ri < len(row_cls) else '')
        tds = ''.join(f'<td class="{"n" if i in num_cols else ""} {hl_cols.get(i, "")}">{c}</td>' for i, c in enumerate(r))
        body += f'<tr class="{"tot" if last else ""} {rc_}">{tds}</tr>'
    return f'<div class="rk-tw"><table class="rk-t"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


# ------------------------------------------------------------------ periode
def period_key(ts, gran):
    ts = pd.Timestamp(ts)
    if gran == 'Bulan': return f'{ts.year}-{ts.month:02d}'
    if gran == 'Kuartal': return f'{ts.year}-Q{(ts.month - 1) // 3 + 1}'
    if gran == 'Semester': return f'{ts.year}-H{1 if ts.month <= 6 else 2}'
    return f'{ts.year}'


def period_bounds(key, gran):
    """-> (start, end) Timestamp, end inklusif (23:59:59)."""
    key = str(key)
    if gran == 'Bulan':
        y, m = int(key[:4]), int(key[5:7]); s = pd.Timestamp(y, m, 1); e = pd.Timestamp(y, m, calendar.monthrange(y, m)[1])
    elif gran == 'Kuartal':
        y, q = int(key[:4]), int(key[-1]); s = pd.Timestamp(y, (q - 1) * 3 + 1, 1); em = q * 3; e = pd.Timestamp(y, em, calendar.monthrange(y, em)[1])
    elif gran == 'Semester':
        y, h = int(key[:4]), int(key[-1]); s = pd.Timestamp(y, 1 if h == 1 else 7, 1); em = 6 if h == 1 else 12; e = pd.Timestamp(y, em, calendar.monthrange(y, em)[1])
    else:
        y = int(key[:4]); s = pd.Timestamp(y, 1, 1); e = pd.Timestamp(y, 12, 31)
    return s, e + pd.Timedelta(hours=23, minutes=59, seconds=59)


def period_label(key, gran):
    key = str(key)
    try:
        if gran == 'Bulan': return f'{MONTH_ID[int(key[5:7]) - 1]} {key[:4]}'
        if gran == 'Kuartal': return f'Kuartal {key[-1]} {key[:4]}'
        if gran == 'Semester': return f'Semester {key[-1]} {key[:4]}'
        return f'Tahun {key[:4]}'
    except Exception:
        return key


def period_options(dates, gran):
    d = pd.to_datetime(pd.Series(dates), errors='coerce').dropna()
    if d.empty: return []
    return sorted({period_key(x, gran) for x in d})


def shortcut_pairs(options, n=3):
    """Pasangan periode berurutan terbaru -> [(p1,p2),...] (maks n)."""
    out = []
    for i in range(len(options) - 1, 0, -1):
        out.append((options[i - 1], options[i]))
        if len(out) >= n: break
    return list(reversed(out))


def slice_dates(df, col, start, end):
    if not isinstance(df, pd.DataFrame) or df.empty or col not in df.columns:
        return df
    d = pd.to_datetime(df[col], errors='coerce')
    return df[((d >= start) & (d <= end)).values].copy()


def compare_insights(m1, m2, l1, l2):
    """m1/m2 dict: ue, core, direct (part+bahan non-PKB), total, rev_ue. -> list item untuk insight_band."""
    g_tot = growth_pct(m2['total'], m1['total'])
    g_ue = growth_pct(m2['ue'], m1['ue'])
    d_tot = m2['total'] - m1['total']
    if g_tot is None: t1 = f'Belum ada pembanding revenue pada <b>{esc(l1)}</b>.'
    elif g_tot >= 0: t1 = f'Total omzet tumbuh <b>{g_tot:+.1f}%</b> ({"+" if d_tot >= 0 else "-"}{fmt_rp(abs(d_tot))}), unit masuk {fmt_growth(g_ue)} dibanding {esc(l1)}.'
    else: t1 = f'Total omzet turun <b>{g_tot:.1f}%</b> ({"-"}{fmt_rp(abs(d_tot))}) dibanding {esc(l1)}; unit masuk {fmt_growth(g_ue)}.'
    sh2 = (m2['direct'] / m2['total'] * 100) if m2['total'] else 0.0
    sh1 = (m1['direct'] / m1['total'] * 100) if m1['total'] else 0.0
    t2 = (f'Penjualan part &amp; bahan tanpa PKB <b>{fmt_rp(m2["direct"])}</b> ({sh2:.1f}% dari total; sebelumnya {sh1:.1f}%).')
    g_y = growth_pct(m2['rev_ue'], m1['rev_ue'])
    t3 = (f'Revenue per UE <b>{fmt_rp(m2["rev_ue"])}</b> ({fmt_growth(g_y)} dari {esc(l1)}).')
    return [('Pertumbuhan Revenue', t1, 'g'), ('Kontribusi Non-PKB', t2, 'o'), ('Yield Produktivitas (Rev/UE)', t3, 'c')]


# ------------------------------------------------------------------ analitik UE
def _col(df, name, default=''):
    return df[name] if isinstance(df, pd.DataFrame) and name in df.columns else pd.Series(default, index=getattr(df, 'index', []))


def _clean_s(s):
    return s.fillna('').astype(str).str.strip()


def model_distribution(df, top=10):
    if not isinstance(df, pd.DataFrame) or df.empty or 'Type Kendaraan' not in df.columns:
        return pd.DataFrame()
    x = df.copy()
    x['_m'] = _clean_s(x['Type Kendaraan'])
    x = x[x['_m'] != '']
    if x.empty: return pd.DataFrame()
    x['UE'] = pd.to_numeric(_col(x, 'UE', 1), errors='coerce').fillna(0)
    x['Revenue'] = pd.to_numeric(_col(x, 'Revenue', 0), errors='coerce').fillna(0)
    x['_j'] = _clean_s(_col(x, 'Jenis Pekerjaan', ''))
    g = x.groupby('_m').agg(UE=('UE', 'sum'), Omzet=('Revenue', 'sum')).reset_index().rename(columns={'_m': 'Model'})
    tot = float(g['UE'].sum())
    g['Porsi'] = g['UE'] / tot * 100 if tot else 0.0
    g['Avg'] = np.where(g['UE'] > 0, g['Omzet'] / g['UE'], 0.0)
    dom = (x[x['_j'] != ''].groupby(['_m', '_j'])['UE'].sum().reset_index().sort_values(['_m', 'UE'], ascending=[True, False]).drop_duplicates('_m').set_index('_m')['_j'])
    g['Pekerjaan Dominan'] = g['Model'].map(dom).fillna('-')
    return g.sort_values('UE', ascending=False).head(top).reset_index(drop=True)


def customer_segments(df):
    """Segmentasi dari kolom 'Customer Type' (jika ada & terisi)."""
    if not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()
    col = next((c for c in ['Customer Type', 'Tipe Customer', 'Segment'] if c in df.columns), None)
    if col is None: return pd.DataFrame()
    x = df.copy()
    x['_s'] = _clean_s(x[col]).replace('', 'Tidak diketahui')
    x['UE'] = pd.to_numeric(_col(x, 'UE', 1), errors='coerce').fillna(0)
    x['Revenue'] = pd.to_numeric(_col(x, 'Revenue', 0), errors='coerce').fillna(0)
    g = x.groupby('_s').agg(UE=('UE', 'sum'), Omzet=('Revenue', 'sum')).reset_index().rename(columns={'_s': 'Segmen'})
    tot = float(g['UE'].sum())
    g['Porsi'] = g['UE'] / tot * 100 if tot else 0.0
    return g.sort_values('UE', ascending=False).reset_index(drop=True)


def dow_workload(df):
    """Rata-rata UE per hari kerja (per tanggal unik) + tingkat kepadatan."""
    if not isinstance(df, pd.DataFrame) or df.empty or 'Tanggal' not in df.columns:
        return pd.DataFrame()
    x = df.copy()
    x['_d'] = pd.to_datetime(x['Tanggal'], errors='coerce').dt.normalize()
    x = x.dropna(subset=['_d'])
    if x.empty: return pd.DataFrame()
    x['UE'] = pd.to_numeric(_col(x, 'UE', 1), errors='coerce').fillna(0)
    per_day = x.groupby('_d')['UE'].sum().reset_index()
    per_day['Hari'] = per_day['_d'].dt.dayofweek.map(lambda i: DAY_ID[int(i)])
    g = per_day.groupby('Hari').agg(Total=('UE', 'sum'), Hari_Kerja=('_d', 'nunique')).reset_index()
    g['Rata2'] = g['Total'] / g['Hari_Kerja']
    mx = float(g['Rata2'].max()) if len(g) else 0.0
    def lvl(v):
        r = v / mx if mx else 0
        return 'Sangat Padat' if r >= .9 else 'Padat' if r >= .7 else 'Sedang' if r >= .45 else 'Lancar'
    g['Level'] = g['Rata2'].map(lvl)
    g['_o'] = g['Hari'].map({d: i for i, d in enumerate(DAY_ID)})
    return g.sort_values('_o').drop(columns='_o').reset_index(drop=True)


# ------------------------------------------------------------------ analitik sparepart
def fast_moving(parts):
    """Gabungan Billing Service (PKB) + Billing Part (counter) per part."""
    need = {'No Part', 'Deskripsi', 'Qty', 'Sales Amount'}
    if not isinstance(parts, pd.DataFrame) or parts.empty or not need.issubset(parts.columns):
        return pd.DataFrame()
    x = parts.copy()
    x['No Part'] = _clean_s(x['No Part']); x['Deskripsi'] = _clean_s(x['Deskripsi'])
    x = x[(x['No Part'] != '') | (x['Deskripsi'] != '')]
    if x.empty: return pd.DataFrame()
    x['Qty'] = pd.to_numeric(x['Qty'], errors='coerce').fillna(0)
    x['Sales Amount'] = pd.to_numeric(x['Sales Amount'], errors='coerce').fillna(0)
    x['GP'] = pd.to_numeric(_col(x, 'Gross Profit', 0), errors='coerce').fillna(0)
    src = _clean_s(_col(x, 'Sumber Penjualan', ''))
    x['QtyPKB'] = np.where(src == 'Billing Service', x['Qty'], 0.0)
    x['QtyCtr'] = np.where(src == 'Billing Part', x['Qty'], 0.0)
    g = x.groupby(['No Part', 'Deskripsi'], dropna=False).agg(QtyPKB=('QtyPKB', 'sum'), QtyCtr=('QtyCtr', 'sum'), Qty=('Qty', 'sum'),
                                                              Omzet=('Sales Amount', 'sum'), GP=('GP', 'sum')).reset_index()
    g['Harga'] = np.where(g['Qty'] > 0, g['Omzet'] / g['Qty'], 0.0)
    g['Margin'] = np.where((g['Omzet'] > 0) & (g['GP'] != 0), g['GP'] / g['Omzet'] * 100, np.nan)
    g = g.sort_values(['Qty', 'Omzet'], ascending=False).reset_index(drop=True)
    tq = float(g['Qty'].sum())
    cum = g['Qty'].cumsum() / tq if tq else pd.Series(1.0, index=g.index)
    prev = cum.shift(1).fillna(0)           # kategori ditentukan oleh posisi AWAL item pada kurva kumulatif
    g['Kategori'] = np.where(prev < .70, 'Fast Moving', np.where(prev < .90, 'Medium Moving', 'Slow Moving'))
    return g


def branch_sparepart(parts, branches):
    rows = []
    has = isinstance(parts, pd.DataFrame) and not parts.empty and 'Sales Amount' in parts.columns
    for b in branches:
        if has and 'Cabang' in parts.columns:
            p = parts[parts['Cabang'].fillna('').astype(str) == b]
            src = p['Sumber Penjualan'] if 'Sumber Penjualan' in p.columns else pd.Series('', index=p.index)
            pk = float(p.loc[src.eq('Billing Service'), 'Sales Amount'].sum()); ct = float(p.loc[src.eq('Billing Part'), 'Sales Amount'].sum())
        else:
            pk = ct = 0.0
        tot = pk + ct
        rows.append({'Cabang': b, 'PKB': pk, 'Counter': ct, 'Total': tot, 'Porsi': (ct / tot * 100 if tot else 0.0)})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ target bulanan
def monthly_series(daily, targets, scope, branches, last_n=6, upto=None):
    """daily: DataFrame index tanggal, kolom UE,Jasa,Part,Bahan,Revenue. targets: {'YYYY-MM': {cabang:{metrik:nilai}}}.
    -> DataFrame per bulan: Key, Label, {m}_A, {m}_T, Pct (revenue)."""
    mets = ['UE', 'Jasa', 'Part', 'Bahan', 'Revenue']
    if not isinstance(daily, pd.DataFrame) or daily.empty:
        return pd.DataFrame()
    d = daily.copy(); d.index = pd.to_datetime(d.index)
    d['_k'] = d.index.strftime('%Y-%m')
    act = d.groupby('_k')[mets].sum()
    keys = sorted(set(act.index) | set(targets.keys()))
    if upto is not None:
        keys = [k for k in keys if k <= upto]
    keys = keys[-last_n:]
    rows = []
    for k in keys:
        tg = targets.get(k, {}) or {}
        bs = list(dict.fromkeys(list(branches) + list(tg.keys()))) if scope == 'Semua Cabang' else [scope]
        r = {'Key': k, 'Label': f'{MON_SHORT[int(k[5:7]) - 1]} {k[:4]}'}
        for m in mets:
            r[m + '_A'] = float(act.loc[k, m]) if k in act.index else 0.0
            r[m + '_T'] = float(sum(float((tg.get(b, {}) or {}).get(m, 0) or 0) for b in bs))
        r['Pct'] = (r['Revenue_A'] / r['Revenue_T'] * 100) if r['Revenue_T'] > 0 else 0.0
        rows.append(r)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ V17b: header halaman & legenda donat
def page_header(period_text, data_text, user_name, role_text='', eyebrow='KHARISMA - WORKSHOP INTELLIGENCE',
                title='KHARISMA WORKSHOP PERFORMANCE',
                desc='Dashboard operasional untuk memantau UE, revenue, parts, bahan, OPL, customer journey dan quality dalam satu tampilan.',
                data_label='DATA PKB'):
    """Kartu header atas halaman (sesuai referensi): judul di kiri; periode, jumlah data, status live dan user di kanan."""
    ini = esc((str(user_name).strip() or '?')[:1].upper())
    return ('<div class="rk-ph"><div class="rk-ph-l">'
            f'<span class="rk-ph-eb">{esc(eyebrow)}</span><div class="rk-ph-t">{esc(title)}</div><p>{esc(desc)}</p></div>'
            '<div class="rk-ph-r">'
            f'<span class="rk-chip dark"><small>PERIODE:</small> {esc(period_text)}</span>'
            f'<span class="rk-chip soft"><small>{esc(data_label)}:</small> {esc(data_text)}</span>'
            '<span class="rk-chip live"><i></i>Live analysis</span>'
            f'<span class="rk-chip user"><b class="av">{ini}</b><span class="nm">{esc(user_name)}<small>{esc(role_text)}</small></span></span>'
            '</div></div>')


def legend_list(items):
    """items: list of (warna_hex, nama, sub, nilai_txt, porsi_txt) -> kartu legenda di samping donat."""
    rows = ''.join(
        f'<div class="rk-lg"><i style="background:{c}"></i><div class="t"><b>{esc(n)}</b><small>{esc(s)}</small></div>'
        f'<div class="v"><b>{esc(v)}</b><small>{esc(p)}</small></div></div>' for c, n, s, v, p in items)
    return f'<div class="rk-lgw">{rows}</div>'


def module_card_head(name, ok, file_txt):
    badge = '<span class="rk-badge green">Siap</span>' if ok else '<span class="rk-badge gray">Belum ada</span>'
    return (f'<div class="rk-mod"><div class="rk-mod-t"><b>{esc(name)}</b>{badge}</div>'
            f'<div class="rk-mod-f">{file_txt}</div></div>')


def share_pct(part, total):
    try:
        return f'{float(part) / float(total) * 100:.0f}%' if float(total) else '0%'
    except Exception:
        return '0%'


def detail_card(label, icon, tone, actual_txt, target_txt, pct, status_txt, status_tone, stats, target_set=True):
    """Kartu detail per metrik: angka besar, progress bar, badge status, dan baris statistik [(label, nilai)]."""
    width = max(0.0, min(pct, 100.0)) if target_set else 0.0
    badge = f'{pct:.1f}%' if target_set else 'belum ada target'
    rows = ''.join(f'<div class="rk-dr"><span>{esc(a)}</span><b>{b}</b></div>' for a, b in stats)
    return (f'<div class="rk-card rk-dc"><div class="rk-top"><span class="rk-lab">{esc(label)}</span>'
            f'<span class="rk-ic {tone}"><span class="msr">{icon}</span></span></div>'
            f'<div class="rk-val">{actual_txt} <small>/ {target_txt}</small></div>'
            f'<div class="rk-row"><span class="rk-badge {status_tone}">{esc(status_txt)}</span><b class="rk-badge {tone if target_set else "gray"}">{badge}</b></div>'
            f'<div class="rk-bar"><i class="{tone if target_set else "gray"}" style="width:{width:.1f}%"></i></div>'
            f'<div class="rk-drs">{rows}</div></div>')


BAHAN_KATS = ['Oli & Pelumas', 'Chemical', 'Bahan Lain-lain']
# Mapping resmi kode bahan -> kategori. Kode di luar dua daftar ini otomatis masuk "Bahan Lain-lain".
BAHAN_KODE = {
    'Oli & Pelumas': ['DGO10M', 'DGO5WM', 'DGO0WM', 'EO01M', 'EO02M', 'EO03M', 'EO01K', 'EO02K', 'EO03K',
                      'CA02M', 'CA01M', 'CA01K', 'CA02K', 'ATF01M', 'AT01M', 'CVT01M', 'AT01K'],
    'Chemical': ['EG01M', 'EX01M', 'FB01M', 'CO01M', 'EP01M', 'WP01M', 'R01M', 'CC01M', 'EC01M',
                 'EG01K', 'EX01K', 'EC01K', 'CC01K', 'FL01K'],
}
BAHAN_KODE_LAIN = BAHAN_KATS[2]


def norm_kode(code):
    """Samakan penulisan kode bahan (huruf besar, tanpa spasi/tanda baca) supaya cocok dengan mapping."""
    return re.sub(r'[^A-Z0-9]', '', str(code or '').upper())


_KODE_TO_KAT = {norm_kode(c): k for k, lst in BAHAN_KODE.items() for c in lst}


BAHAN_MANUAL = {}   # mapping manual {kode ternormalisasi: kategori}; diisi aplikasi dari file simpanan, diutamakan di atas daftar resmi


def bahan_kategori(code, name=''):
    """Klasifikasi bahan berdasarkan KODE: mapping manual > daftar resmi (BAHAN_KODE) > Bahan Lain-lain."""
    k = norm_kode(code)
    m = BAHAN_MANUAL.get(k)
    if m in BAHAN_KATS: return m
    return _KODE_TO_KAT.get(k, BAHAN_KODE_LAIN)


def min_card(label, value, sub='', tone='blue'):
    """Kartu metrik minimalis: tanpa latar, hanya garis aksen di kiri."""
    sb = f'<span class="s">{sub}</span>' if sub else ''
    return f'<div class="rk-mn {tone}"><span class="l">{esc(label)}</span><span class="v">{value}</span>{sb}</div>'


def min_grid(cards):
    return '<div class="rk-mg">' + ''.join(cards) + '</div>'


# ------------------------------------------------------------------ V23: Management Insight (analisa & strategi UE + revenue)
def mi_status(actual, target, elapsed, days_in):
    """Status satu metrik (UE / Revenue / Rev per UE) terhadap target bulanan dan pace linear per hari kalender."""
    actual = float(actual or 0); target = float(target or 0)
    days_left = max(int(days_in) - int(elapsed), 0)
    pct = (actual / target * 100) if target > 0 else 0.0
    exp = (elapsed / days_in * 100) if days_in else 0.0
    pace = (pct / exp * 100) if (exp > 0 and target > 0) else 0.0
    remain = max(target - actual, 0.0)
    need = (remain / days_left) if days_left > 0 else remain
    run = (actual / elapsed) if elapsed > 0 else 0.0
    proj = run * days_in
    if target <= 0: lab, tone = 'Target kosong', 'gray'
    elif pct >= 100: lab, tone = 'Tercapai', 'green'
    elif pace >= 100: lab, tone = 'Di atas pace', 'green'
    elif pace >= 90: lab, tone = 'Mendekati pace', 'orange'
    else: lab, tone = 'Tertinggal', 'red'
    return dict(actual=actual, target=target, pct=pct, exp=exp, pace=pace, remain=remain, need=need, run=run, proj=proj,
                proj_pct=(proj / target * 100) if target > 0 else 0.0, days_left=days_left, label=lab, tone=tone,
                daily_target=(target / days_in) if days_in else 0.0)


def mi_strategy(T, R, elapsed, days_in, ctx=None):
    """Analisa gap + strategi agar UE & Revenue mencapai target. Fungsi murni (tanpa Streamlit).
    T/R: dict metrik -> target / realisasi (UE, Jasa, Part, Bahan, Revenue). ctx: data pendukung (opsional)."""
    ctx = ctx or {}
    s_ue = mi_status(R.get('UE', 0), T.get('UE', 0), elapsed, days_in)
    s_rev = mi_status(R.get('Revenue', 0), T.get('Revenue', 0), elapsed, days_in)
    rpu_a = (R.get('Revenue', 0) / R['UE']) if R.get('UE', 0) else 0.0
    rpu_t = (T.get('Revenue', 0) / T['UE']) if T.get('UE', 0) > 0 and T.get('Revenue', 0) > 0 else 0.0
    yld = (rpu_a / rpu_t * 100) if rpu_t > 0 else 0.0
    s_rpu = dict(actual=rpu_a, target=rpu_t, pct=yld, label=('Target kosong' if rpu_t <= 0 else ('Di atas target' if yld >= 100 else 'Mendekati' if yld >= 90 else 'Di bawah target')),
                 tone=('gray' if rpu_t <= 0 else 'green' if yld >= 100 else 'orange' if yld >= 90 else 'red'))
    has_t = (T.get('UE', 0) > 0) or (T.get('Revenue', 0) > 0)

    # ---- diagnosis penyebab gap ----
    if not has_t or elapsed <= 0: cause = 'nodata'
    elif s_rev['pct'] >= 100 or s_rev['pace'] >= 100: cause = 'aman'
    else:
        vg = 100 - s_ue['pace'] if T.get('UE', 0) > 0 else 0.0
        yg = 100 - yld if rpu_t > 0 else 0.0
        cause = 'volume' if vg > yg + 3 else 'yield' if yg > vg + 3 else 'keduanya'
    cause_text = {
        'nodata': 'Target bulan ini belum diinput, sehingga diagnosis gap belum dapat dihitung. Isi target lewat <b>Target &amp; Pencapaian → Input Target</b>.',
        'aman': 'Revenue berada <b>di atas / sesuai pace</b>. Fokus: pertahankan ritme harian dan lindungi yield (Rev/UE) agar tidak turun di akhir bulan.',
        'volume': f'Revenue tertinggal terutama karena <b>volume UE</b> (UE {s_ue["pace"]:.0f}% dari pace) sementara yield Rev/UE {yld:.0f}% dari target. Prioritas: <b>tambah unit masuk</b>.',
        'yield': f'Revenue tertinggal terutama karena <b>yield per unit</b> (Rev/UE {yld:.0f}% dari target) sementara UE {s_ue["pace"]:.0f}% dari pace. Prioritas: <b>naikkan nilai tiap unit</b>.',
        'keduanya': f'Revenue tertinggal karena <b>volume dan yield sama-sama di bawah target</b> (UE {s_ue["pace"]:.0f}% dari pace, Rev/UE {yld:.0f}% dari target). Perlu dorongan di kedua sisi.',
    }[cause]

    # ---- komponen revenue ----
    comps = []
    for m in ('Jasa', 'Part', 'Bahan'):
        t = float(T.get(m, 0) or 0); a = float(R.get(m, 0) or 0)
        comps.append(dict(name=m, actual=a, target=t, pct=(a / t * 100) if t > 0 else None))
    withT = [c for c in comps if c['pct'] is not None]
    lowest = min(withT, key=lambda c: c['pct']) if withT else None

    # ---- skenario mengejar target revenue ----
    scen = []
    ue_day = (R.get('UE', 0) / elapsed) if elapsed > 0 else 0.0
    run_rev = s_rev['run']; need_rev = s_rev['need']
    if has_t and T.get('Revenue', 0) > 0 and s_rev['pct'] < 100 and s_rev['days_left'] > 0 and run_rev > 0:
        f = need_rev / run_rev
        scen.append(dict(title='A. Fokus Volume UE', tone='blue',
                         value=f'{ue_day * f:,.1f} UE / hari', sub=f'dari {ue_day:,.1f} UE/hari sekarang (+{ue_day * (f - 1):,.1f} UE/hari atau {(f - 1) * 100:+.0f}%) dengan Rev/UE tetap {fmt_rp(rpu_a)}.'))
        scen.append(dict(title='B. Fokus Yield (Rev/UE)', tone='green',
                         value=f'{fmt_rp(rpu_a * f)} / UE', sub=f'naik {fmt_rp(rpu_a * (f - 1))} per unit ({(f - 1) * 100:+.0f}%) dengan volume tetap {ue_day:,.1f} UE/hari.'))
        g = f ** 0.5
        scen.append(dict(title='C. Kombinasi Seimbang (disarankan)', tone='purple',
                         value=f'UE {(g - 1) * 100:+.1f}% &amp; Rev/UE {(g - 1) * 100:+.1f}%', sub=f'≈ {ue_day * g:,.1f} UE/hari &amp; {fmt_rp(rpu_a * g)}/UE. Beban terbagi, paling realistis dicapai.'))
    scen_note = ('' if scen else ('Target revenue sudah tercapai.' if (has_t and s_rev['pct'] >= 100) else
                 'Skenario muncul setelah target revenue diinput dan ada realisasi berjalan.' if not has_t else 'Tidak ada sisa hari untuk mengejar target bulan ini.'))

    # ---- strategi (6 tuas) ----
    bk = ctx.get('booking_pct'); wd = ctx.get('weak_day'); avg_d = ctx.get('avg_day_ue')
    nonp = ctx.get('nonpkb_share'); dpart = ctx.get('direct_part', 0.0); dbahan = ctx.get('direct_bahan', 0.0)
    sa_lo = ctx.get('sa_low'); sa_hi = ctx.get('sa_high'); sa_n = int(ctx.get('sa_n', 0) or 0); nos = int(ctx.get('no_sales', 0) or 0)
    ue_need_day = s_ue['need'] if T.get('UE', 0) > 0 and s_ue['days_left'] > 0 else None
    P = {'volume': ('Prioritas Utama', 'red'), 'yield': ('Prioritas Utama', 'red'), 'keduanya': ('Prioritas Utama', 'red')}
    def prio(kind):
        if cause in ('volume', 'yield', 'keduanya'):
            return ('Prioritas Utama', 'red') if (cause == kind or cause == 'keduanya') else ('Pendukung', 'blue')
        if cause == 'aman': return ('Pertahankan', 'green')
        return ('Rekomendasi', 'gray')
    ev1 = [f'UE aktual rata-rata <b>{ue_day:,.1f}/hari</b>' + (f'; kebutuhan sisa bulan <b>{ue_need_day:,.1f}/hari</b> (target harian {s_ue["daily_target"]:,.1f}).' if ue_need_day is not None else '.')]
    if bk is not None: ev1.append(f'Rasio booking <b>{bk:.1f}%</b> dari UE.')
    if wd: ev1.append(f'Hari paling sepi: <b>{wd[0]}</b> (~{wd[1]:.0f} UE)' + (f' vs rata-rata {avg_d:.0f} UE/hari.' if avg_d else '.'))
    ev2 = [f'Rev/UE aktual <b>{fmt_rp(rpu_a)}</b>' + (f' vs kebutuhan target <b>{fmt_rp(rpu_t)}</b> ({yld:.0f}%).' if rpu_t > 0 else '.')]
    if sa_hi and sa_lo and sa_hi[0] != sa_lo[0]: ev2.append(f'SA tertinggi {sa_hi[0]} ({fmt_rp(sa_hi[1])}/UE), terendah {sa_lo[0]} ({fmt_rp(sa_lo[1])}/UE).')
    ev3 = [f'Non-PKB menyumbang <b>{nonp:.1f}%</b> revenue (Part {fmt_rp(dpart)} • Bahan {fmt_rp(dbahan)}).' if nonp is not None else 'Data non-PKB belum tersedia.']
    comp_actions = {
        'Jasa': ['Maksimalkan jam kerja produktif teknisi dan pangkas waktu tunggu stall agar kapasitas jasa terpakai penuh.',
                 'Dorong pekerjaan berbasis jasa (service berkala, AC, kaki-kaki, tune-up) dan terapkan tarif jasa secara konsisten.',
                 'Tinjau diskon jasa; pastikan tidak melewati batas kebijakan.'],
        'Part': ['Pastikan ketersediaan part fast-moving dan part kebutuhan service berkala (hindari indent).',
                 'Tawarkan part genuine pada estimasi dengan opsi harga; catat penolakan untuk follow-up.',
                 'Tentukan stok minimum untuk 10 part terlaris (lihat halaman Sparepart).'],
        'Bahan': ['Standarkan penawaran oli &amp; chemical (flush, additive) di setiap service.',
                  'Pastikan bahan yang di-issue ke PKB tercatat dan ditagihkan penuh.',
                  'Dorong penjualan consumable non-PKB ke bengkel rekanan (lihat Top 10 Bahan).'],
    }
    if lowest:
        ev4 = [f'<b>{lowest["name"]}</b> baru <b>{lowest["pct"]:.0f}%</b> dari target (' + ', '.join(f'{c["name"]} {c["pct"]:.0f}%' for c in withT) + ').']
        act4 = comp_actions[lowest['name']]; title4 = f'Kejar Komponen Tertinggal: {lowest["name"]}'
    else:
        ev4 = ['Target per komponen (Jasa, Part, Bahan) belum diinput.']
        act4 = ['Input target Jasa, Part, dan Bahan agar komponen yang tertinggal dapat dideteksi otomatis.',
                'Sementara itu pantau komposisi revenue dan fokus pada komponen berkontribusi terbesar.']
        title4 = 'Kejar Komponen yang Tertinggal'
    sa_daily = (s_ue['daily_target'] / sa_n) if (sa_n and s_ue['daily_target']) else None
    ev5 = [f'{sa_n} Service Advisor aktif' + (f'; target rata-rata <b>{sa_daily:,.1f} UE/SA/hari</b>.' if sa_daily else '.')]
    ev6 = [f'<b>{nos:,}</b> PKB tanpa penjualan (tidak dihitung UE/revenue).' if nos else 'Tidak ada PKB tanpa penjualan pada data aktif.']
    levers = [
        dict(icon='event_available', tone='blue', title='Naikkan Volume UE: Booking & Kedatangan Unit', prio=prio('volume'), evidence=ev1,
             actions=['Kirim reminder service berkala (H-7 dan H-1) via WhatsApp/telepon ke pelanggan yang jatuh tempo, dari database Customer/PKB.',
                      'Dorong booking: beri slot prioritas dan estimasi waktu pasti; targetkan rasio booking naik bertahap tiap minggu.',
                      f'Isi hari sepi{" (" + wd[0] + ")" if wd else ""} dengan promo/paket khusus dan jadwal booking armada perusahaan.',
                      'Follow-up unit yang batal/ditunda dan pelanggan yang tidak kembali lebih dari 6 bulan (win-back).',
                      'Jalin kerja sama armada, perusahaan, dan komunitas untuk volume terjadwal.'],
             kpi=(f'Ukuran: UE ≥ {ue_need_day:,.1f}/hari sisa bulan ini; rasio booking naik tiap minggu.' if ue_need_day is not None else 'Ukuran: UE harian ≥ target harian; rasio booking naik tiap minggu.')),
        dict(icon='payments', tone='green', title='Naikkan Revenue per UE: Upselling & Paket Layanan', prio=prio('yield'), evidence=ev2,
             actions=['Wajibkan inspeksi/checklist saat penerimaan dan tawarkan pekerjaan tambahan sesuai temuan (rem, filter, aki, AC, wiper, dll.).',
                      'Siapkan paket layanan (oli + filter, tune-up, AC, rem) dengan harga paket agar nilai tiket naik.',
                      'Beri estimasi dua opsi (hemat vs lengkap) supaya pelanggan memilih, bukan menolak.',
                      'Pasang target Rev/UE per SA dan tampilkan papan pencapaian; SA terendah didampingi SA terbaik.',
                      'Pastikan semua pekerjaan tambahan masuk estimasi dan PKB (cegah kebocoran revenue).'],
             kpi=(f'Ukuran: Rev/UE ≥ {fmt_rp(rpu_t)}.' if rpu_t > 0 else 'Ukuran: Rev/UE naik dibanding bulan lalu.')),
        dict(icon='storefront', tone='orange', title='Maksimalkan Penjualan Non-PKB (Counter Part & Bahan)', prio=('Pendukung', 'blue') if cause != 'nodata' else ('Rekomendasi', 'gray'), evidence=ev3,
             actions=['Petakan bengkel rekanan, toko, dan pelanggan counter; tawarkan part fast-moving serta oli/chemical (lihat Top 10 di halaman Sparepart/Bahan).',
                      'Jaga stok fast-moving dengan titik pemesanan ulang agar tidak kehilangan penjualan.',
                      'Buat bundling consumable (oli + chemical) dan harga bertingkat untuk pembelian grosir.',
                      'Jadwalkan kunjungan/penawaran mingguan dan kirim katalog harga via WhatsApp.'],
             kpi='Ukuran: kontribusi Non-PKB naik; tidak ada kehabisan stok fast-moving.'),
        dict(icon='build', tone='red', title=title4, prio=('Prioritas Utama', 'red') if (lowest and cause in ('volume', 'yield', 'keduanya')) else ('Pendukung', 'blue') if lowest else ('Rekomendasi', 'gray'), evidence=ev4, actions=act4,
             kpi='Ukuran: pencapaian komponen mendekati pace bulanan.'),
        dict(icon='groups', tone='purple', title='Produktivitas Service Advisor & Kapasitas Bengkel', prio=('Pendukung', 'blue') if cause != 'nodata' else ('Rekomendasi', 'gray'), evidence=ev5,
             actions=['Daily huddle 10 menit tiap pagi: capaian kemarin vs target harian, unit booking hari ini, dan target per SA.',
                      'Leaderboard mingguan UE dan Rev/UE per SA; apresiasi yang konsisten, coaching untuk yang tertinggal.',
                      'Atur pembagian unit dan jadwal teknisi agar tidak ada antrean pada hari padat dan stall kosong pada hari sepi.'],
             kpi=(f'Ukuran: rata-rata ≥ {sa_daily:,.1f} UE per SA per hari.' if sa_daily else 'Ukuran: UE per SA per hari mencapai target.')),
        dict(icon='fact_check', tone='teal', title='Disiplin Data & Closing Harian', prio=('Pendukung', 'blue') if cause != 'nodata' else ('Rekomendasi', 'gray'), evidence=ev6,
             actions=['Closing PKB setiap hari agar UE dan revenue langsung terhitung.',
                      'Upload Laporan Estimasi SA setiap hari; hari yang belum diupload belum terhitung di dashboard.',
                      'Review PKB tanpa penjualan setiap H+1 dan selesaikan penyebabnya (batal, belum invoice, dll.).'],
             kpi='Ukuran: PKB tanpa penjualan mendekati nol; tidak ada tanggal kosong.'),
    ]

    # ---- rencana aksi ----
    dt_ue = s_ue['daily_target']; dt_rev = s_rev['daily_target']
    wdn = wd[0] if wd else 'hari sepi'
    add_ue = (ue_need_day - ue_day) if ue_need_day is not None else None
    plan = [
        ['Daily huddle: evaluasi capaian kemarin vs target harian', 'Kepala Bengkel + semua SA', 'Harian (pagi)', (f'UE ≥ {dt_ue:,.1f}/hari • Revenue ≥ {fmt_rp(dt_rev)}/hari' if dt_ue else 'Capaian harian tercatat'), 'UE &amp; Revenue'],
        ['Reminder &amp; booking service berkala', 'SA / CRM', 'Harian', (f'Reminder terkirim ≥ {max(add_ue, 0) * 2:,.0f}/hari (asumsi konversi ±50%, sesuaikan)' if add_ue is not None else 'Jumlah reminder &amp; booking tercatat'), 'UE'],
        ['Checklist inspeksi &amp; upselling pada setiap unit', 'SA', 'Setiap unit masuk', (f'Rev/UE ≥ {fmt_rp(rpu_t)}' if rpu_t > 0 else 'Rev/UE naik'), 'Revenue per UE'],
        [f'Promo/paket khusus hari {wdn} &amp; booking armada', 'Kepala Bengkel / Marketing', 'Mingguan', (f'UE hari {wdn} naik mendekati rata-rata {avg_d:.0f} UE' if (wd and avg_d) else 'UE hari sepi naik'), 'UE'],
        ['Penawaran counter sales part &amp; bahan ke rekanan', 'Sales Part / Admin Part', 'Mingguan', 'Kontribusi Non-PKB naik; stok fast-moving aman', 'Revenue'],
        ['Review pace &amp; koreksi strategi', 'Branch Manager', 'Mingguan (Senin)', 'Pace UE &amp; Revenue ≥ 100%', 'UE &amp; Revenue'],
        ['Closing PKB &amp; upload Laporan Estimasi SA', 'Admin', 'Harian', 'PKB tanpa penjualan → 0; tanggal kosong → 0', 'Akurasi data'],
        ['Evaluasi akhir bulan &amp; penetapan target bulan depan', 'Manajemen', 'Bulanan', 'Target realistis berdasarkan tren 3–6 bulan', 'UE &amp; Revenue'],
    ]
    # ---- early warning (jika → maka) ----
    trig = [
        ['Pencapaian kumulatif UE atau Revenue &lt; 90% dari pace', 'Eskalasi ke Branch Manager; aktifkan program booking + promo hari sepi minggu itu juga.'],
        [(f'UE harian &lt; {dt_ue * 0.8:,.1f} (80% target harian) 3 hari berturut-turut' if dt_ue else 'UE harian turun 3 hari berturut-turut'), 'Telepon pelanggan jatuh tempo service dan armada langganan hari itu; cek penyebab (cuaca, kapasitas, stok part).'],
        [(f'Rev/UE harian &lt; {fmt_rp(rpu_t * 0.95)} (95% target)' if rpu_t > 0 else 'Rev/UE harian turun &gt; 5% dari rata-rata bulan'), 'Briefing ulang upselling; audit estimasi SA dan pekerjaan tambahan yang tidak masuk PKB.'],
        ['Rasio booking turun dibanding bulan lalu', 'Perkuat reminder H-7/H-1 dan beri slot prioritas booking.'],
        ['Part atau bahan fast-moving kosong', 'Pesan darurat dan tawarkan alternatif; catat kehilangan penjualan.'],
        ['Pace tetap &lt; 90% memasuki pekan terakhir', 'Fokus pada skenario kombinasi: kejar unit tertunda, closing PKB, dan penawaran Non-PKB ke rekanan.'],
    ]
    return dict(s_ue=s_ue, s_rev=s_rev, s_rpu=s_rpu, cause=cause, cause_text=cause_text, comps=comps, lowest=lowest, scen=scen, scen_note=scen_note,
                levers=levers, plan=plan, trig=trig, has_target=has_t)
