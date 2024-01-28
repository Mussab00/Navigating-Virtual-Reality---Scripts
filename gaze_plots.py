import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd


def create_gaze_plots(input_path, output_path):
    data = pd.read_excel(input_path)
    data['Timestamp in Minutes'] = data['Recording timestamp'] / 60000000
    data['Event Change'] = (data['Eye movement type'] != data['Eye movement type'].shift(1)) | \
                            (data['Gaze event duration'] != data['Gaze event duration'].shift(1))

    fixations = data[data['Eye movement type'] == 'Fixation']
    saccades = data[data['Eye movement type'] == 'Saccade']

    distinct_fixation_count = fixations.groupby(fixations['Timestamp in Minutes'].astype(int))['Event Change'].sum()
    distinct_saccade_count = saccades.groupby(saccades['Timestamp in Minutes'].astype(int))['Event Change'].sum()

    distinct_fixations = data[(data['Eye movement type'] == 'Fixation') & data['Event Change']]
    distinct_saccades = data[(data['Eye movement type'] == 'Saccade') & data['Event Change']]


    plt.figure(figsize=(7, 24))  # Adjust the size as needed

    # Subplot 1: Heatmap of Gaze Points
    plt.subplot(5, 1, 1)  # 3 rows, 2 columns, 1st subplot
    sns.kdeplot(x=data['Gaze point X'], y=data['Gaze point Y'], cmap="Blues", shade=True, bw_adjust=0.5)
    plt.title('Heatmap of Gaze Points')
    plt.xlabel('Gaze Point X')
    plt.ylabel('Gaze Point Y')

    # Subplot 2: Pupil Diameter Change Over Time
    plt.subplot(5, 1, 2)
    plt.plot(data['Timestamp in Minutes'], data['Pupil diameter left'], label='Left Pupil')
    plt.plot(data['Timestamp in Minutes'], data['Pupil diameter right'], label='Right Pupil')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Pupil Diameter')
    plt.title('Pupil Diameter Change Over Time')
    plt.legend()

    # Subplot 3: Distinct Fixation Duration
    plt.subplot(5, 1, 3)
    plt.plot(distinct_fixations['Timestamp in Minutes'], distinct_fixations['Gaze event duration'], color='blue')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Duration (Milliseconds)')
    plt.title('Duration of Distinct Fixations Over Time')

    # Subplot 4: Distinct Saccade Duration
    plt.subplot(5, 1, 4)
    plt.plot(distinct_saccades['Timestamp in Minutes'], distinct_saccades['Gaze event duration'], color='orange')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Duration (Milliseconds)')
    plt.title('Duration of Distinct Saccades Over Time')

    # Subplot 5: Fixation and Saccade Count per Minute
    plt.subplot(5, 1, 5)
    plt.bar(distinct_fixation_count.index - 0.2, distinct_fixation_count, width=0.4, label='Fixations')
    plt.bar(distinct_saccade_count.index + 0.2, distinct_saccade_count, width=0.4, color='orange', label='Saccades')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Distinct Count')
    plt.title('Fixation and Saccade Count per Minute')
    plt.legend()

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig(output_path + '/gaze graphs.png')
    plt.clf()