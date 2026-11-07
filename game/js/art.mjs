/* Original ink drawings in the approved flat style. Supplied SVGs are inlined elsewhere, untouched. */

var INK = "#10170F";

function wrap(inner) {
  return "<svg viewBox='0 0 64 64' class='drawn' aria-hidden='true'>" + inner + "</svg>";
}

function clock(text, extra) {
  return wrap(
    "<rect x='4' y='14' width='56' height='36' rx='6' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/>" +
    "<text x='32' y='38' text-anchor='middle' font-size='14' font-family='Lilita One,sans-serif' fill='" + INK + "' stroke='none'>" + text + "</text>" +
    (extra || "")
  );
}

var DRAWN = {
  "baby-scale-8": wrap("<rect x='8' y='28' width='48' height='22' rx='4' fill='#D9DEE3' stroke='" + INK + "' stroke-width='3'/><rect x='18' y='16' width='28' height='14' rx='3' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><text x='32' y='28' text-anchor='middle' font-size='10' fill='" + INK + "' stroke='none'>8 lb</text>"),
  blanket: wrap("<path d='M8 18h48v30H8z' fill='#C46B4A' stroke='" + INK + "' stroke-width='3'/><path d='M8 28h48M8 38h48M24 18v30M40 18v30' stroke='#8A4630' stroke-width='2' fill='none'/>"),
  "blanket-white": wrap("<path d='M8 18h48v30H8z' fill='#F4F1EA' stroke='" + INK + "' stroke-width='3'/><path d='M8 28h48M8 38h48M24 18v30M40 18v30' stroke='#8A939C' stroke-width='2' fill='none'/>"),
  "clock-530": clock("5:30", "<path d='M10 8h10l2 8H12z' fill='#C46B4A' stroke='" + INK + "' stroke-width='2'/>"),
  "clock-930": clock("9:30", ""),
  "clock-1100": clock("11:00", "<circle cx='52' cy='12' r='5' fill='#FFCC33' stroke='" + INK + "' stroke-width='2'/>"),
  "clock-730": clock("7:30", "<ellipse cx='12' cy='12' rx='7' ry='3' fill='#5B6670' stroke='" + INK + "' stroke-width='2'/>"),
  "crowd-5000": wrap("<rect x='6' y='8' width='52' height='14' rx='2' fill='#FFCC33' stroke='" + INK + "' stroke-width='2'/><text x='32' y='18' text-anchor='middle' font-size='10' fill='" + INK + "' stroke='none'>5,000</text><g fill='#3E5A7A' stroke='" + INK + "' stroke-width='1'>" + [0, 1, 2, 3, 4, 5, 6, 7].map(function (i) { return "<circle cx='" + (10 + (i % 4) * 14) + "' cy='" + (32 + Math.floor(i / 4) * 14) + "' r='4'/>"; }).join("") + "</g>"),
  diaper: wrap("<path d='M14 16h36v22c0 10-8 16-18 16S14 48 14 38z' fill='#F7F4EE' stroke='" + INK + "' stroke-width='3'/><path d='M14 24h8M42 24h8' stroke='" + INK + "' stroke-width='3'/>"),
  "door-13": wrap("<rect x='16' y='6' width='32' height='52' rx='2' fill='#C46B4A' stroke='" + INK + "' stroke-width='3'/><rect x='22' y='14' width='20' height='14' rx='2' fill='#F6E9C8' stroke='" + INK + "' stroke-width='2'/><text x='32' y='25' text-anchor='middle' font-size='12' fill='" + INK + "' stroke='none'>13</text><circle cx='40' cy='36' r='2' fill='#FFCC33' stroke='" + INK + "'/>"),
  "floor-4": wrap("<rect x='14' y='8' width='36' height='48' rx='4' fill='#2C3F56' stroke='" + INK + "' stroke-width='3'/><circle cx='32' cy='24' r='8' fill='#FFCC33' stroke='" + INK + "' stroke-width='2'/><text x='32' y='28' text-anchor='middle' font-size='12' fill='" + INK + "' stroke='none'>4</text><circle cx='32' cy='44' r='6' fill='#1A1F24' stroke='#B9C2CA' stroke-width='2'/>"),
  glass: wrap("<path d='M20 8h24l-4 36a8 8 0 0 1-16 0z' fill='#D7F3FF' stroke='" + INK + "' stroke-width='3'/><path d='M18 28h28' stroke='#7FB8D4' stroke-width='3'/>"),
  "high-five": wrap("<path d='M6 40c8-16 14-16 18-6 2-12 8-14 12-4 2-10 10-10 12 2 0-8 8-8 10 4 6 8 4 18-6 22-18-2-40-6-46-18z' fill='#F2C1A0' stroke='" + INK + "' stroke-width='3'/>"),
  hungry: wrap("<circle cx='24' cy='26' r='12' fill='#F2C1A0' stroke='" + INK + "' stroke-width='3'/><path d='M18 28c2 3 8 3 10 0' stroke='" + INK + "' fill='none'/><ellipse cx='44' cy='44' rx='14' ry='6' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><path d='M40 36c6 2 10 6 8 10' stroke='" + INK + "' fill='none'/>"),
  "light-rays": wrap("<circle cx='32' cy='32' r='10' fill='#FFCC33' stroke='" + INK + "' stroke-width='3'/>" + [0, 45, 90, 135].map(function (d) { return "<path d='M32 32l18 -4' stroke='#FFCC33' stroke-width='4' transform='rotate(" + d + " 32 32)'/>"; }).join("")),
  "line-queue": wrap("<path d='M8 20h48v28H8z' fill='none' stroke='#FFCC33' stroke-width='3'/>" + [0, 1, 2, 3, 4, 5, 6].map(function (i) { return "<circle cx='" + (14 + i * 6) + "' cy='34' r='3' fill='#3E5A7A' stroke='" + INK + "'/>"; }).join("")),
  "money-120": wrap("<rect x='6' y='10' width='52' height='44' rx='4' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><text x='32' y='28' text-anchor='middle' font-size='10' fill='" + INK + "' stroke='none'>1 night</text><text x='32' y='46' text-anchor='middle' font-size='14' fill='" + INK + "' stroke='none'>$120</text>"),
  "money-50": wrap("<rect x='4' y='16' width='56' height='32' rx='4' fill='#2FA84F' stroke='" + INK + "' stroke-width='3'/><text x='32' y='38' text-anchor='middle' font-size='18' fill='#F6E9C8' stroke='none'>50</text>"),
  "number-14": wrap("<rect x='6' y='10' width='52' height='44' rx='4' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><text x='32' y='42' text-anchor='middle' font-size='22' fill='" + INK + "' stroke='none'>14</text>"),
  "number-15": wrap("<rect x='6' y='10' width='52' height='44' rx='4' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><text x='32' y='42' text-anchor='middle' font-size='22' fill='" + INK + "' stroke='none'>15</text>"),
  "number-16": wrap("<rect x='6' y='10' width='52' height='44' rx='4' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><text x='32' y='42' text-anchor='middle' font-size='22' fill='" + INK + "' stroke='none'>16</text>"),
  "number-17": wrap("<rect x='6' y='10' width='52' height='44' rx='4' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><text x='32' y='42' text-anchor='middle' font-size='22' fill='" + INK + "' stroke='none'>17</text>"),
  "number-19": wrap("<rect x='6' y='10' width='52' height='44' rx='4' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/><text x='32' y='42' text-anchor='middle' font-size='22' fill='" + INK + "' stroke='none'>19</text>"),
  nurse: wrap("<rect x='22' y='16' width='20' height='16' rx='4' fill='#F4F1EA' stroke='" + INK + "' stroke-width='3'/><path d='M16 32h32v22H16z' fill='#7FB8F5' stroke='" + INK + "' stroke-width='3'/><rect x='40' y='36' width='12' height='16' rx='2' fill='#F6E9C8' stroke='" + INK + "' stroke-width='2'/>"),
  "pray-kneel": wrap("<circle cx='32' cy='16' r='7' fill='#F2C1A0' stroke='" + INK + "' stroke-width='3'/><path d='M24 28c6 8 10 20 8 28H28L24 36z' fill='#3E5A7A' stroke='" + INK + "' stroke-width='3'/><path d='M28 34h8l2 6' stroke='" + INK + "' fill='none'/>"),
  "pray-meal": wrap("<rect x='8' y='36' width='48' height='8' fill='#6B4423' stroke='" + INK + "' stroke-width='3'/><circle cx='18' cy='24' r='6' fill='#F2C1A0' stroke='" + INK + "'/><circle cx='32' cy='22' r='6' fill='#F2C1A0' stroke='" + INK + "'/><circle cx='46' cy='24' r='6' fill='#F2C1A0' stroke='" + INK + "'/><ellipse cx='32' cy='40' rx='8' ry='3' fill='#F6E9C8' stroke='" + INK + "'/>"),
  "shape-line": wrap("<path d='M6 32h52' stroke='" + INK + "' stroke-width='8' stroke-linecap='round'/>"),
  "size-big": wrap("<circle cx='32' cy='32' r='28' fill='#E23B3B' stroke='" + INK + "' stroke-width='3'/>"),
  "size-long": wrap("<rect x='2' y='28' width='60' height='8' rx='3' fill='#6B4423' stroke='" + INK + "' stroke-width='3'/>"),
  "size-small": wrap("<circle cx='32' cy='32' r='6' fill='#E23B3B' stroke='" + INK + "' stroke-width='3'/>"),
  "swatch-gold": wrap("<rect x='8' y='12' width='48' height='40' rx='4' fill='#FFC400' stroke='" + INK + "' stroke-width='3'/><path d='M12 20h40' stroke='#FFF8E1' stroke-width='4'/>"),
  "swatch-pink": wrap("<rect x='8' y='12' width='48' height='40' rx='4' fill='#FF8FC7' stroke='" + INK + "' stroke-width='3'/>"),
  they: wrap("<circle cx='14' cy='40' r='5' fill='#3E5A7A' stroke='" + INK + "'/><circle cx='24' cy='42' r='5' fill='#3E5A7A' stroke='" + INK + "'/><path d='M22 36l10-8' stroke='" + INK + "' stroke-width='3'/><circle cx='42' cy='24' r='4' fill='#C46B4A' stroke='" + INK + "'/><circle cx='50' cy='28' r='4' fill='#2FA84F' stroke='" + INK + "'/><circle cx='46' cy='18' r='4' fill='#F5D06B' stroke='" + INK + "'/>"),
  "chef-hat": wrap("<path d='M16 36c-6-2-8-12-2-16 0-8 12-12 18-8 8-6 20 0 18 10 8 2 8 14 0 16z' fill='#FFF8E7' stroke='" + INK + "' stroke-width='3'/><rect x='18' y='36' width='28' height='8' fill='#FFC400' stroke='" + INK + "' stroke-width='3'/>"),
  "gem-emerald": wrap("<rect x='18' y='16' width='28' height='32' fill='#00D26A' stroke='" + INK + "' stroke-width='3'/><path d='M18 28h28' stroke='#0B6B32' stroke-width='3'/>"),
  "gem-amethyst": wrap("<ellipse cx='32' cy='32' rx='14' ry='18' fill='#A020F0' stroke='" + INK + "' stroke-width='3'/>"),
  "gem-sapphire": wrap("<circle cx='32' cy='32' r='16' fill='#1E5BFF' stroke='" + INK + "' stroke-width='3'/>"),
  "gem-ruby": wrap("<rect x='16' y='16' width='32' height='32' rx='6' fill='#FF2E63' stroke='" + INK + "' stroke-width='3'/>"),
  "gem-topaz": wrap("<path d='M32 8l16 28-16 20L16 36z' fill='#FFC400' stroke='" + INK + "' stroke-width='3'/>"),
  "cape-green": wrap("<path d='M32 10l18 8-6 36H20L14 18z' fill='#17633A' stroke='" + INK + "' stroke-width='3'/><circle cx='32' cy='16' r='3' fill='#FFCC33' stroke='" + INK + "'/>"),
  "cape-purple": wrap("<path d='M32 10l18 8-6 36H20L14 18z' fill='#6D3CC9' stroke='" + INK + "' stroke-width='3'/><circle cx='26' cy='30' r='2' fill='#fff' stroke='none'/><circle cx='36' cy='38' r='2' fill='#fff' stroke='none'/>"),
  "cape-sky": wrap("<path d='M32 10l18 8-6 36H20L14 18z' fill='#7FB8F5' stroke='" + INK + "' stroke-width='3'/><path d='M18 40h28' stroke='#F4F1EA' stroke-width='3'/>"),
  coin: wrap("<circle cx='32' cy='32' r='18' fill='#FFCC33' stroke='#B7860B' stroke-width='4'/><path d='M32 18l3 8h8l-6 5 2 8-7-5-7 5 2-8-6-5h8z' fill='#FFF8E1' stroke='" + INK + "' stroke-width='1'/>"),
  "sword-iron": wrap("<path d='M30 6h4v32h-4z' fill='#C5CDD4' stroke='" + INK + "' stroke-width='3'/><path d='M22 38h20' stroke='" + INK + "' stroke-width='4'/><rect x='29' y='40' width='6' height='14' fill='#6B4423' stroke='" + INK + "'/>"),
  "shield-sunrise": wrap("<circle cx='32' cy='32' r='20' fill='#3D7FD9' stroke='" + INK + "' stroke-width='3'/><path d='M32 20l3 8h8l-6 5 2 8-7-4-7 4 2-8-6-5h8z' fill='#FFCC33' stroke='" + INK + "' stroke-width='1'/>")
};

export function drawnSvg(id) {
  return DRAWN[id] || wrap("<rect x='12' y='12' width='40' height='40' rx='6' fill='#E9D9AE' stroke='" + INK + "' stroke-width='3'/>");
}

export function pictureHtml(pic, inline) {
  if (!pic) return "";
  if (String(pic).indexOf("svg:") === 0) {
    var id = String(pic).slice(4);
    if (inline && inline[id]) return "<div class='pic-svg supplied'>" + inline[id] + "</div>";
    return "<div class='pic-svg'>" + drawnSvg(id) + "</div>";
  }
  return "<div class='emoji-pic' aria-hidden='true'>" + escapeText(pic) + "</div>";
}

export function escapeText(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

var SKY = {
  m: ["#8EC6F5", "#E7F4FF", "#3E8F45"],
  d: ["#6EB6EA", "#F4FBFF", "#46A04C"],
  a: ["#F0B56A", "#F8E2B0", "#3E8F45"],
  e: ["#E07A4A", "#F6C7A1", "#2C6B3A"],
  n: ["#0B1B33", "#0F3B4A", "#123F35"]
};

function sky(tod) {
  var c = SKY[tod] || SKY.m;
  return "<rect width='390' height='520' fill='" + c[1] + "'/><rect width='390' height='340' fill='" + c[0] + "'/>";
}

function ground(tod) {
  var g = (SKY[tod] || SKY.m)[2];
  return "<path d='M0 340h390v180H0z' fill='" + g + "' stroke='" + INK + "' stroke-width='3'/>" +
    "<path d='M0 348c40 8 30-6 70 0s40 10 70 0 40-10 80 0 50 8 80-2 40-6 90 4v-12H0z' fill='#2F6E38' opacity='.35'/>";
}

function tree(x) {
  return "<rect x='" + (x + 10) + "' y='300' width='22' height='120' fill='#4E3018' stroke='" + INK + "' stroke-width='3'/>" +
    "<circle cx='" + (x + 21) + "' cy='300' r='34' fill='#17633A' stroke='" + INK + "' stroke-width='3'/>" +
    "<path d='M" + (x + 8) + " 400h26l-4 16h-18z' fill='#3E2612' stroke='" + INK + "' stroke-width='2'/>";
}
export function guardianKneel(tint) {
  var color = tint || "#7FD38B";
  return "<svg class='guardian' viewBox='0 0 140 160' aria-hidden='true'>" +
    "<ellipse cx='74' cy='148' rx='40' ry='8' fill='#10170F' opacity='.28'/>" +
    "<path d='M46 118c-16 8-22 18-10 24 18 4 40-6 36-18z' fill='" + color + "' stroke='#10170F' stroke-width='3'/>" +
    "<path d='M58 86h36l6 28H50z' fill='" + color + "' stroke='#10170F' stroke-width='3'/>" +
    "<path d='M62 78h28l4 10H58z' fill='#2C3F56' stroke='#10170F' stroke-width='3'/>" +
    "<circle cx='76' cy='58' r='16' fill='#F2C1A0' stroke='#10170F' stroke-width='3'/>" +
    "<path d='M62 50h28v10c0 8-28 8-28 0z' fill='#2C3F56' stroke='#10170F' stroke-width='3'/>" +
    "<circle cx='112' cy='96' r='18' fill='" + color + "' stroke='#10170F' stroke-width='3'/>" +
    "<circle cx='112' cy='96' r='8' fill='#FFCC33' stroke='#10170F' stroke-width='3'/>" +
    "<path d='M40 108c-8 10-6 22 4 24' fill='none' stroke='#10170F' stroke-width='3'/>" +
    "</svg>";
}

var ZONE_MARK = {
  phonics: "<path d='M18 40c8-16 20-16 28 0' fill='none' stroke='#10170F' stroke-width='3'/><path d='M24 40c4-8 12-8 16 0' fill='none' stroke='#10170F' stroke-width='3'/><circle cx='32' cy='44' r='4' fill='#7FD38B' stroke='#10170F' stroke-width='3'/>",
  "sight-words": "<path d='M10 18h20v28H10zM34 18h20v28H34z' fill='#F6E9C8' stroke='#10170F' stroke-width='3'/><path d='M30 18v28' stroke='#10170F' stroke-width='3'/>",
  "colors-shapes": "<circle cx='20' cy='34' r='10' fill='#F5A3C7' stroke='#10170F' stroke-width='3'/><rect x='34' y='24' width='18' height='18' fill='#7FB8F5' stroke='#10170F' stroke-width='3'/>",
  numbers: "<path d='M18 16v32M28 16v32M38 16v32M14 26h32M14 38h32' fill='none' stroke='#10170F' stroke-width='3'/>",
  "baby-hospital": "<path d='M12 28h40v16H12z' fill='#F2B8A0' stroke='#10170F' stroke-width='3'/><path d='M12 28c8-10 32-10 40 0' fill='none' stroke='#10170F' stroke-width='3'/>",
  "maxwell-says": "<rect x='14' y='20' width='36' height='24' fill='#E7D3A1' stroke='#10170F' stroke-width='3'/><path d='M22 44h20' stroke='#10170F' stroke-width='3'/>",
  soundDuel: "<path d='M16 44l12-20 12 20zM32 44l10-16 10 16z' fill='#6B5CA5' stroke='#10170F' stroke-width='3'/>"
};

export function zoneEmblem(zone) {
  if (zone && zone.emblem && String(zone.emblem).indexOf("svg:") === 0) {
    return "<div class='pic-svg'>" + drawnSvg(String(zone.emblem).slice(4)) + "</div>";
  }
  var mark = ZONE_MARK[(zone && zone.key) || ""] || ZONE_MARK.phonics;
  return "<svg class='ico emblem-svg' viewBox='0 0 64 64' aria-hidden='true'>" + mark + "</svg>";
}

export function sceneSvg(kind, tod) {
  var t = tod || "m";
  if (kind === "forest" && (t === "m" || t === "d")) t = "n";
  var parts = [sky(t)];
  if (kind === "park" || kind === "pond" || kind === "farm") {
    parts.push(ground(t));
    parts.push(tree(8));
    parts.push(tree(300));
  }
  if (kind === "pond") {
    parts.push("<ellipse cx='250' cy='430' rx='70' ry='22' fill='#4A9BE0' stroke='" + INK + "' stroke-width='3'/>");
    parts.push("<ellipse cx='250' cy='430' rx='36' ry='8' fill='none' stroke='#E7F4FF' stroke-width='2'/>");
  }
  if (kind === "farm") {
    parts.push("<rect x='18' y='360' width='14' height='70' fill='#8A6A3A' stroke='" + INK + "'/><rect x='78' y='360' width='14' height='70' fill='#8A6A3A' stroke='" + INK + "'/><path d='M25 400h60' stroke='#8A6A3A' stroke-width='6'/>");
    parts.push("<path d='M130 400c6-36 16-36 22 0M160 400c6-44 16-44 22 0' stroke='#E8B84A' stroke-width='4' fill='none'/>");
  }
  if (kind === "home" || kind === "kitchen" || kind === "desk") {
    parts.push("<rect width='390' height='520' fill='#E7D3A1'/>");
    parts.push("<rect y='180' width='390' height='340' fill='#F6E9C8' stroke='" + INK + "' stroke-width='3'/>");
    parts.push("<rect x='250' y='200' width='90' height='60' fill='#B9D7F2' stroke='" + INK + "' stroke-width='3'/>");
    parts.push("<rect y='360' width='390' height='160' fill='#C4A574' stroke='" + INK + "' stroke-width='3'/>");
  }
  if (kind === "desk") {
    parts.push("<rect x='40' y='210' width='40' height='160' fill='#8A5A32' stroke='" + INK + "' stroke-width='3'/>");
    parts.push("<rect x='48' y='250' width='26' height='16' fill='#FFCC33' stroke='" + INK + "'/><text x='61' y='262' text-anchor='middle' font-size='11' fill='" + INK + "' stroke='none'>13</text>");
  }
  if (kind === "kitchen") {
    parts.push("<rect x='40' y='330' width='90' height='12' fill='#6B4423' stroke='" + INK + "' stroke-width='3'/>");
  }
  if (kind === "home") {
    parts.push("<rect x='30' y='300' width='80' height='12' fill='#6B4423' stroke='" + INK + "' stroke-width='3'/>");
  }
  if (kind === "forest") {
    parts = [sky("n"), "<rect y='340' width='390' height='180' fill='#123F35' stroke='" + INK + "' stroke-width='3'/>"];
    parts.push(tree(4));
    parts.push(tree(80));
    parts.push(tree(280));
    parts.push("<path d='M150 300h130' stroke='#3E2612' stroke-width='8'/>");
    parts.push("<path d='M40 430l24 40h-48z' fill='#C46B4A' stroke='" + INK + "' stroke-width='3'/>");
  }
  parts.push("<ellipse cx='90' cy='470' rx='28' ry='6' fill='#10170F' opacity='.25'/>");
  return "<svg class='scene-svg' viewBox='0 0 390 520' preserveAspectRatio='none' aria-hidden='true'>" + parts.join("") + "</svg>";
}

export function coinRow(filled) {
  var html = "";
  for (var i = 0; i < 10; i++) {
    html += "<span class='coin" + (i < filled ? " on" : "") + "'>" + drawnSvg("coin") + "</span>";
  }
  return "<span class='coins' aria-hidden='true'>" + html + "</span>";
}
