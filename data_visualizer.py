import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = np.arctan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = np.arcsin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = np.arctan2(t3, t4)

    return roll_x, pitch_y, yaw_z

def create_e4_plots(input_path, output_path):
    df = pd.read_csv(input_path, sep=';')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    df = df.interpolate()

    required_columns = ['LeftTick', 'RightTick', 'RotationX', 'RotationY', 'RotationZ', 'RotationW']
    for column in required_columns:
        if column not in df.columns:
            df[column] = np.nan

    non_null_non_zero = df[(df['LeftTick'].notna() & df['LeftTick'].ne(0)) |
                           (df['RightTick'].notna() & df['RightTick'].ne(0))]

    start_index = non_null_non_zero.index[0] if not non_null_non_zero.empty else 0

    df = df.loc[start_index:len(df) - 2]

    if {'RotationX', 'RotationY', 'RotationZ', 'RotationW'}.issubset(df.columns):
        df['roll_x'], df['pitch_y'], df['yaw_z'] = zip(*df.apply(lambda row: quaternion_to_euler(row['RotationX'], row['RotationY'], row['RotationZ'], row['RotationW']), axis=1))

    try:
        df['Elapsed'] = (df['Timestamp'] - df['Timestamp'].iloc[start_index]).dt.total_seconds() / 60
        time_column = 'Elapsed'
    except:
        time_column = 'Timestamp'

    columns_to_plot = {
        'BVP': ('gray', 'BVP'),
        'EDA': ('green', 'EDA'),
        'HR': ('brown', 'HR'),
        'TEMP': ('purple', 'TEMP'),
        'FPS': ('orange', 'FPS'),
        'TicksDiff': ('maroon', 'Wheelchair Rotation'),
        'Comfort Level': ('red', 'Sickness Level (1-4)'),
        'yaw_z': ('cyan', 'Yaw'),
        'pitch_y': ('magenta', 'Pitch'),
        'roll_x': ('blue', 'Roll')
    }

    if 'LeftTick' in df.columns and 'RightTick' in df.columns:
        columns_to_plot['LeftTick'] = ('blue', 'LeftTick and RightTick')
        columns_to_plot.pop('RightTick', None)


    existing_columns = [col for col in columns_to_plot if col in df.columns]
    num_subplots = len(existing_columns)

    fig, axs = plt.subplots(num_subplots, 1, figsize=(12, 24))

    def plot_column(ax, column_name):
        color, title = columns_to_plot[column_name]
        if column_name in ['LeftTick', 'RightTick']:
            ax.plot(df[time_column], df['LeftTick'], color='blue', label='LeftTick')
            ax.plot(df[time_column], df['RightTick'], color='red', label='RightTick')
            ax.legend()
            ax.axhline(0, color='black', linewidth=1)
        else:
            ax.plot(df[time_column], df[column_name], color=color)
        ax.set_title(title)
        ax.set_xlabel('Time Elapsed (minutes)')

    for i, column in enumerate(existing_columns):
        plot_column(axs[i], column)

    plt.tight_layout()
    plt.savefig(output_path + '/other plots.png')
