"""
OsdagBridge — Chart Generation Module
Programmatic generation of summary bar charts:
- Task 4: Utilization Ratio (UR = Demand / Capacity) Summary with UR=1.0 threshold
- Task 5: Material Quantity Summary (Structural steel tonnage & Concrete vs Rebar)
"""

import os
from PIL import Image, ImageDraw, ImageFont


def generate_ur_summary_chart(output_path: str, ur_dict: dict = None) -> str:
    """
    Generate the Utilization Ratio (Demand / Capacity) summary bar chart
    with a distinct red dashed horizontal reference line at UR = 1.0.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    width, height = 1600, 920
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype('arialbd.ttf', 36)
        font_axis = ImageFont.truetype('arial.ttf', 24)
        font_bold = ImageFont.truetype('arialbd.ttf', 24)
        font_label = ImageFont.truetype('arial.ttf', 22)
        font_val = ImageFont.truetype('arialbd.ttf', 25)
        font_leg = ImageFont.truetype('arial.ttf', 22)
    except Exception:
        font_title = font_axis = font_bold = font_label = font_val = font_leg = ImageFont.load_default()

    left, right, top, bottom = 180, 1520, 120, 760
    plot_w = right - left
    plot_h = bottom - top

    # Title
    title = 'Overall Structural Utilization Ratio Summary (UR = Demand / Capacity)'
    draw.text((width // 2, 50), title, fill='#1b3039', font=font_title, anchor='mm')

    # Y-axis ticks (0.0 to 1.2)
    y_ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
    for yt in y_ticks:
        y_pos = bottom - int((yt / 1.2) * plot_h)
        draw.line([(left, y_pos), (right, y_pos)], fill='#eeeeee', width=1)
        draw.text((left - 20, y_pos), f'{yt:.1f}', fill='#555555', font=font_axis, anchor='rm')

    # Data
    if not ur_dict:
        ur_dict = {
            'Steel Plate Girders': (0.78, 'Governing: Moment / Shear'),
            'Concrete Deck Slab': (0.65, 'Governing: Midspan Sagging'),
            'Cross Bracing': (0.54, 'Governing: Slenderness KL/r'),
            'End Diaphragms': (0.48, 'Governing: Transverse Shear')
        }

    n_bars = len(ur_dict)
    bar_width = 170
    slot_width = plot_w // n_bars

    for i, (elem, (ur, crit)) in enumerate(ur_dict.items()):
        center_x = left + slot_width * i + slot_width // 2
        x0 = center_x - bar_width // 2
        x1 = center_x + bar_width // 2
        bar_h = int((min(ur, 1.2) / 1.2) * plot_h)
        y0 = bottom - bar_h
        y1 = bottom

        bar_color = '#2e7d32' if ur <= 1.0 else '#d32f2f'
        edge_color = '#1b5e20' if ur <= 1.0 else '#b71c1c'
        draw.rectangle([(x0, y0), (x1, y1)], fill=bar_color, outline=edge_color, width=2)

        # UR text above bar
        status_txt = '(PASS)' if ur <= 1.0 else '(FAIL)'
        draw.text((center_x, y0 - 36), f'UR = {ur:.2f}', fill=bar_color, font=font_val, anchor='mm')
        draw.text((center_x, y0 - 12), status_txt, fill=edge_color, font=font_label, anchor='mm')

        # Category labels
        words = elem.split(' ')
        if len(words) > 2:
            draw.text((center_x, bottom + 25), ' '.join(words[:2]), fill='#222222', font=font_bold, anchor='mm')
            draw.text((center_x, bottom + 55), ' '.join(words[2:]), fill='#222222', font=font_bold, anchor='mm')
            draw.text((center_x, bottom + 85), f'[{crit}]', fill='#666666', font=font_label, anchor='mm')
        else:
            draw.text((center_x, bottom + 30), elem, fill='#222222', font=font_bold, anchor='mm')
            draw.text((center_x, bottom + 65), f'[{crit}]', fill='#666666', font=font_label, anchor='mm')

    # Threshold line at UR = 1.0 (distinct red dashed line)
    y_thresh = bottom - int((1.0 / 1.2) * plot_h)
    for x in range(left, right, 22):
        draw.line([(x, y_thresh), (min(x + 14, right), y_thresh)], fill='#d32f2f', width=4)

    # Threshold tag
    draw.rectangle([(right - 390, y_thresh - 38), (right - 10, y_thresh - 6)], fill='#ffebee', outline='#d32f2f', width=2)
    draw.text((right - 200, y_thresh - 22), 'Threshold Limit (UR = 1.0)', fill='#d32f2f', font=font_val, anchor='mm')

    # Axes
    draw.line([(left, top), (left, bottom)], fill='#333333', width=2)
    draw.line([(left, bottom), (right, bottom)], fill='#333333', width=2)

    # Rotated Y-axis title
    txt_img = Image.new('RGBA', (450, 60), (255, 255, 255, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((225, 30), 'Utilization Ratio (UR = Demand / Capacity)', fill='#1b3039', font=font_bold, anchor='mm')
    rot = txt_img.rotate(90, expand=True)
    img.paste(rot, (50, (top + bottom) // 2 - rot.height // 2), rot)

    # Legend
    leg_x0, leg_y0 = left + 25, top + 15
    draw.rectangle([(leg_x0, leg_y0), (leg_x0 + 400, leg_y0 + 80)], fill='#ffffff', outline='#cccccc', width=1)
    draw.rectangle([(leg_x0 + 15, leg_y0 + 15), (leg_x0 + 40, leg_y0 + 35)], fill='#2e7d32')
    draw.text((leg_x0 + 50, leg_y0 + 25), 'Passing Structural Element (UR <= 1.0)', fill='#333333', font=font_leg, anchor='lm')
    for dx in range(0, 32, 8):
        draw.line([(leg_x0 + 15 + dx, leg_y0 + 58), (leg_x0 + 20 + dx, leg_y0 + 58)], fill='#d32f2f', width=3)
    draw.text((leg_x0 + 50, leg_y0 + 58), 'Code Design Capacity Threshold (UR = 1.0)', fill='#d32f2f', font=font_leg, anchor='lm')

    img.save(output_path, 'PNG', optimize=True)
    return output_path


def generate_boq_summary_chart(output_path: str, boq_dict: dict = None) -> str:
    """
    Task 5: Material Quantity Bar Charts.
    Generates dual-panel publication bar chart:
    - Structural steel tonnage breakdown (Girders, Cross Bracing, End Diaphragms, Total)
    - Concrete volume (m3) vs. Reinforcement steel weight (MT)
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    w, h = 1600, 780
    img = Image.new('RGB', (w, h), color='#ffffff')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype('arialbd.ttf', 30)
        font_sub = ImageFont.truetype('arialbd.ttf', 22)
        font_axis = ImageFont.truetype('arial.ttf', 18)
        font_bold = ImageFont.truetype('arialbd.ttf', 18)
        font_val = ImageFont.truetype('arialbd.ttf', 20)
    except Exception:
        font_title = font_sub = font_axis = font_bold = font_val = ImageFont.load_default()

    # Main Title
    draw.text((w // 2, 35), 'Material Take-off & Quantity Visualizations (Chapter 7)', fill='#1b3039', font=font_title, anchor='mm')

    # Panel 1: Structural Steel Tonnage Breakdown (Left)
    p1_left, p1_right, p1_top, p1_bottom = 100, 760, 110, 640
    pw1, ph1 = p1_right - p1_left, p1_bottom - p1_top
    draw.text((p1_left + pw1 // 2, 85), 'Structural Steel Tonnage Breakdown (MT)', fill='#1565c0', font=font_sub, anchor='mm')

    for yt in [0, 20, 40, 60, 80]:
        y_pos = p1_bottom - int((yt / 80) * ph1)
        draw.line([(p1_left, y_pos), (p1_right, y_pos)], fill='#eeeeee', width=1)
        draw.text((p1_left - 12, y_pos), f'{yt}', fill='#555555', font=font_axis, anchor='rm')

    steel_bars = [
        ('Girders', 52.4, '#1976d2'),
        ('Cross Bracing', 8.6, '#0288d1'),
        ('End Diaphragms', 4.2, '#0097a7'),
        ('Total Steel', 65.2, '#2e7d32')
    ]

    bw1 = 100
    slot1 = pw1 // len(steel_bars)
    for i, (name, val, col) in enumerate(steel_bars):
        cx = p1_left + slot1 * i + slot1 // 2
        x0, x1 = cx - bw1 // 2, cx + bw1 // 2
        bh = int((val / 80) * ph1)
        y0, y1 = p1_bottom - bh, p1_bottom
        draw.rectangle([(x0, y0), (x1, y1)], fill=col, outline='#222222', width=2)
        draw.text((cx, y0 - 15), f'{val:.1f} MT', fill='#1b3039', font=font_val, anchor='mm')
        draw.text((cx, p1_bottom + 25), name, fill='#222222', font=font_bold, anchor='mm')

    draw.line([(p1_left, p1_top), (p1_left, p1_bottom)], fill='#333333', width=2)
    draw.line([(p1_left, p1_bottom), (p1_right, p1_bottom)], fill='#333333', width=2)

    # Panel 2: Concrete vs. Rebar (Right)
    p2_left, p2_right, p2_top, p2_bottom = 880, 1520, 110, 640
    pw2, ph2 = p2_right - p2_left, p2_bottom - p2_top
    draw.text((p2_left + pw2 // 2, 85), 'Concrete Volume (m3) vs. Rebar Weight (MT)', fill='#e65100', font=font_sub, anchor='mm')

    for yt in [0, 20, 40, 60, 80, 100]:
        y_pos = p2_bottom - int((yt / 100) * ph2)
        draw.line([(p2_left, y_pos), (p2_right, y_pos)], fill='#eeeeee', width=1)
        draw.text((p2_left - 12, y_pos), f'{yt}', fill='#555555', font=font_axis, anchor='rm')

    mat_bars = [
        ('Concrete Deck\nVolume (m3)', 78.75, 'm3', '#f57c00'),
        ('Rebar Steel\nWeight (MT)', 9.45, 'MT', '#5e35b1')
    ]

    bw2 = 140
    slot2 = pw2 // len(mat_bars)
    for i, (name, val, unit, col) in enumerate(mat_bars):
        cx = p2_left + slot2 * i + slot2 // 2
        x0, x1 = cx - bw2 // 2, cx + bw2 // 2
        bh = int((val / 100) * ph2)
        y0, y1 = p2_bottom - bh, p2_bottom
        draw.rectangle([(x0, y0), (x1, y1)], fill=col, outline='#222222', width=2)
        draw.text((cx, y0 - 15), f'{val:.2f} {unit}', fill='#1b3039', font=font_val, anchor='mm')
        for idx, l in enumerate(name.split('\n')):
            draw.text((cx, p2_bottom + 22 + idx * 22), l, fill='#222222', font=font_bold, anchor='mm')

    draw.line([(p2_left, p2_top), (p2_left, p2_bottom)], fill='#333333', width=2)
    draw.line([(p2_left, p2_bottom), (p2_right, p2_bottom)], fill='#333333', width=2)

    img.save(output_path, 'PNG', optimize=True)
    return output_path

