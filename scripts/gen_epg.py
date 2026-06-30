#!/usr/bin/env python3
# Genera xmltv.xml para el demo de OnePlay, SIEMPRE centrado en la hora actual (UTC).
# Portable (macOS y el runner Linux del GitHub Action). Lo ejecuta el workflow refresh-epg cada 6h.
from datetime import datetime, timezone, timedelta
from xml.sax.saxutils import escape

# (epg_channel_id, display-name)
CHANNELS = [
    ("france24.en", "FRANCE 24 English"),
    ("dw.en",       "DW English"),
    ("cgtn.en",     "CGTN News"),
    ("bloomberg.us","Bloomberg TV"),
    ("france24.es", "FRANCE 24 Espanol"),
    ("dw.es",       "DW Espanol"),
    ("france24.fr", "FRANCE 24 Francais"),
    ("dw.de",       "DW Deutsch"),
    ("nasa.tv",     "NASA TV Public"),
    ("nasamedia.tv","NASA TV Media"),
    ("redbull.tv",  "Red Bull TV"),
]

TITLES = {
    "france24.en": ["France 24 News","The World This Week","The Debate","Business Daily","Sport 24","The Interview","Encore!","Reporters","Down to Earth","Talking Europe","Eye on Africa","Access Asia"],
    "dw.en":       ["DW News","The Day","DW Business","Tomorrow Today","Euromaxx","Made in Germany","DocFilm","Sports Life","Arts Unveiled","Eco India","Close Up","Shift"],
    "cgtn.en":     ["CGTN News","The World Today","Global Business","Dialogue","Sports Scene","Culture Express","Tech It Out","The Hub","Full Frame","World Insight","China 24","Across China"],
    "bloomberg.us":["Bloomberg Markets","Balance of Power","Bloomberg Technology","Wall Street Week","Bloomberg Surveillance","The Close","Daybreak","Quicktake","Open Interest","Big Take","Markets Live","Businessweek"],
    "france24.es": ["Noticias France 24","El Debate","Economico","A Fondo","Reporteros","Entre Nosotros","Actualidad","Cultura","Mundo","Express","Aqui Europa","Sin Fronteras"],
    "dw.es":       ["DW Noticias","Al Dia","Economia","Enfoque Europa","Cultura 21","Hecho en Alemania","DocFilm","Vida Sana","En Forma","Global 3000","A Fondo","Camarera"],
    "france24.fr": ["Journal France 24","Le Debat","Economie","Reporters","Element Terre","L'Entretien","Paris Direct","Ici l'Europe","Le Gros Mot","Vous etes ici","Express Orient","A l'Affiche"],
    "dw.de":       ["DW Nachrichten","Der Tag","DW Wirtschaft","Tomorrow Today","Euromaxx","Made in Germany","DokFilm","Sportreportage","Kultur 21","Eco Africa","Close Up","Shift"],
    "nasa.tv":     ["NASA Live: ISS","Mission Briefing","Spacewalk Coverage","Space Station Update","Artemis Update","Launch Coverage","Science Live","Earth from Space","Astronaut Q and A","NASA Explorers","Mission Control","Live Views"],
    "nasamedia.tv":["Solar System Tour","Hubble Highlights","Mars Report","Webb Telescope","Apollo Archives","Universe Today","Galaxy Files","Cosmic Front","Deep Space","Planetary Science","Our Universe","Space Now"],
    "redbull.tv":  ["Cliff Diving World Series","Surfing World Tour","Red Bull Rampage","Motocross Live","Freeski World Tour","Red Bull Air Race","Skate Generation","Crashed Ice","MotoGP Files","Who Is JOB","Danny MacAskill","The Ultimate Ride"],
}

# Ventana amplia para aguantar retrasos del cron: desde -4h hasta +20h (24 bloques de 1h).
HOURS_BACK = 4
SPAN = 24
now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
base = now - timedelta(hours=HOURS_BACK)

def fmt(dt): return dt.strftime("%Y%m%d%H%M%S") + " +0000"

lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv generator-info-name="OnePlay Demo EPG">']
for cid, name in CHANNELS:
    lines.append(f'  <channel id="{cid}"><display-name>{escape(name)}</display-name></channel>')
for cid, _ in CHANNELS:
    titles = TITLES[cid]
    for i in range(SPAN):
        s = base + timedelta(hours=i)
        e = base + timedelta(hours=i + 1)
        t = escape(titles[i % len(titles)])
        lines.append(f'  <programme start="{fmt(s)}" stop="{fmt(e)}" channel="{cid}">')
        lines.append(f'    <title>{t}</title>')
        lines.append(f'    <desc>{t} — en directo.</desc>')
        lines.append('  </programme>')
lines.append('</tv>')

with open("xmltv.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"xmltv.xml generado: {len(CHANNELS)} canales, {len(CHANNELS)*SPAN} programas, ventana {fmt(base)} .. {fmt(base + timedelta(hours=SPAN))}")
