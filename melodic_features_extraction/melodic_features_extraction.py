import os, sys

sys.path.append(r'G:\university\programming files\py files\musicpy\musicpy')
import musicpy as mp
import numpy as np
from copy import deepcopy as copy
from matplotlib import pyplot as plt


class Melody:

    def __init__(self, current_chord, filename=None, is_melody=False):
        if not is_melody:
            try:
                current_chord_melody = mp.alg.split_melody(current_chord)
                current_chord_melody.start_time = current_chord.start_time
            except:
                pass
        self.current_chord = current_chord_melody
        self.filename = filename
        self.percentile = [1, 99]
        self.octave_distribution_tol = 0.85
        self.get_melodic_features()

    def get_melodic_features(self):
        self.pitch_intervals = [
            self.current_chord.notes[i].degree -
            self.current_chord.notes[i - 1].degree
            for i in range(1, len(self.current_chord))
        ]
        self.abs_pitch_intervals = [abs(i) for i in self.pitch_intervals]

        current_degree = self.current_chord.get_degree()
        current_degree_percentile = [
            np.percentile(current_degree, self.percentile[0]),
            np.percentile(current_degree, self.percentile[1])
        ]
        current_degree_preprocess = [
            i for i in current_degree if
            current_degree_percentile[0] <= i <= current_degree_percentile[1]
        ]

        self.pitch_mean = np.mean(current_degree_preprocess)
        self.pitch_var = np.var(current_degree)
        self.pitch_std = np.std(current_degree)
        self.pitch_range = max(current_degree) - min(current_degree)

        current_octave_distribution = [
            (i, len([j for j in self.current_chord if j.num == i]) /
             len(self.current_chord)) for i in range(9)
        ]
        current_octave_distribution.sort(key=lambda s: s[1], reverse=True)
        current_octave_counter = 0
        self.pitch_octave_distribution = []
        for each in current_octave_distribution:
            current_octave_counter += each[1]
            self.pitch_octave_distribution.append(each[0])
            if current_octave_counter >= self.octave_distribution_tol:
                break
        self.pitch_octave_distribution.sort()

        self.pitch_interval_mean = np.mean(self.abs_pitch_intervals)
        self.pitch_interval_var = np.var(self.abs_pitch_intervals)
        self.pitch_interval_std = np.std(self.abs_pitch_intervals)
        self.pitch_interval_distribution = {
            j: self.abs_pitch_intervals.count(i)
            for i, j in mp.database.INTERVAL.items()
        }

        current_interval = self.current_chord.interval
        self.interval_var = np.var(current_interval)
        self.interval_std = np.std(current_interval)
        current_interval_percentile = [
            np.percentile(current_interval, self.percentile[0]),
            np.percentile(current_interval, self.percentile[1])
        ]
        current_interval_preprocess = [
            i for i in current_interval if current_interval_percentile[0] <= i
            <= current_interval_percentile[1]
        ]
        self.interval_mean = np.mean(current_interval_preprocess)

        current_duration = self.current_chord.get_duration()
        self.duration_var = np.var(current_duration)
        self.duration_std = np.std(current_duration)
        current_duration_percentile = [
            np.percentile(current_duration, self.percentile[0]),
            np.percentile(current_duration, self.percentile[1])
        ]
        current_duration_preprocess = [
            i for i in current_duration if current_duration_percentile[0] <= i
            <= current_duration_percentile[1]
        ]
        self.duration_mean = np.mean(current_duration_preprocess)

    def get_key_rate(self, current_scale, bar_range=None):
        current_chord = self.current_chord
        if bar_range is not None:
            current_chord = self.current_chord.cut(*bar_range)
        current_scale_names = current_scale.names()
        current_scale_names = [
            mp.database.standard_dict.get(i, i) for i in current_scale_names
        ]
        current_chord_names = current_chord.names()
        current_chord_names = [
            mp.database.standard_dict.get(i, i) for i in current_chord_names
        ]
        current_key_rate = len([
            i for i in current_chord_names if i in current_scale_names
        ]) / len(current_chord_names)
        return current_key_rate

    def get_moving_melodic_features(self,
                                    width=1,
                                    bar_interval=1,
                                    key_rate_scale=None):
        temp = copy(self)
        start = temp.current_chord.start_time
        length = temp.current_chord.bars(
            start_time=temp.current_chord.start_time)
        results = []
        i = start + bar_interval
        reach_end = False
        while True:
            if i >= length:
                i = length
                reach_end = True
            current_start = i - width
            if current_start < 0:
                current_start = 0
            current_stop = i
            current_melody = copy(temp)
            current_melody.current_chord = current_melody.current_chord.cut(
                current_start, current_stop)
            current_melody.get_melodic_features()
            if key_rate_scale is not None:
                current_key_rate = current_melody.get_key_rate(key_rate_scale)
                current_melody.key_rate = current_key_rate
            results.append(current_melody)
            if reach_end:
                break
            i += bar_interval
        return results


def get_melody_from_file(current_file):
    current = mp.read(current_file)
    current_track = current.tracks[0]
    current_track.start_time = current.start_times[0]
    current_melody = Melody(current_track, filename=current_file)
    return current_melody


def test_get_melodic_features_of_midi_files(midi_path):
    files = [os.path.join(midi_path, i) for i in os.listdir(midi_path)]
    melody_list = []
    for each in files:
        try:
            current = mp.read(each)
        except:
            continue
        if len(current) == 1:
            current_track = current.tracks[0]
            current_track.start_time = current.start_times[0]
            current_melody = Melody(current_track, filename=each)
            melody_list.append(current_melody)
    return melody_list


def test_plot_moving_melodic_features(current_file,
                                      current_width=4,
                                      current_bar_interval=1 / 4,
                                      feature='pitch_mean',
                                      plot_bar_ticks=2,
                                      key_rate_scale=None):
    current = mp.read(current_file)
    current_track = current.tracks[0]
    current_track.start_time = current.start_times[0]
    current_melody = Melody(current_track)
    current_melody_length = current_melody.current_chord.bars(
        current_melody.current_chord.start_time)
    moving_melodic_features = current_melody.get_moving_melodic_features(
        width=current_width,
        bar_interval=current_bar_interval,
        key_rate_scale=key_rate_scale)
    features = [getattr(i, feature) for i in moving_melodic_features]
    points = [
        current_melody.current_chord.start_time + i * current_bar_interval
        for i in range(0,
                       int(current_melody_length / current_bar_interval) - 1)
    ]
    fig = plt.figure(figsize=(12, 8))
    plt.plot(points, features)
    plt.xlabel('bar')
    if feature == 'key_rate':
        plt.ylabel(f'{feature} ({key_rate_scale.get_scale_name()})')
    else:
        plt.ylabel(feature)
    x_major_locator = plt.MultipleLocator(plot_bar_ticks)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.show()


def test_plot_multiple_moving_melodic_features(current_file,
                                               current_width=4,
                                               current_bar_interval=1 / 4,
                                               features=['pitch_mean'],
                                               plot_bar_ticks=2,
                                               key_rate_scale=None):
    current = mp.read(current_file)
    current_track = current.tracks[0]
    current_track.start_time = current.start_times[0]
    current_melody = Melody(current_track)
    current_melody_length = current_melody.current_chord.bars(
        current_melody.current_chord.start_time)
    fig, axes = plt.subplots(len(features), figsize=(12, 8))
    if len(features) == 1:
        axes = [axes]
    if key_rate_scale is None:
        moving_melodic_features = current_melody.get_moving_melodic_features(
            width=current_width, bar_interval=current_bar_interval)
    points = [
        current_melody.current_chord.start_time + i * current_bar_interval
        for i in range(0,
                       int(current_melody_length / current_bar_interval) - 1)
    ]
    for j, feature in enumerate(features):
        if key_rate_scale is not None:
            moving_melodic_features = current_melody.get_moving_melodic_features(
                width=current_width,
                bar_interval=current_bar_interval,
                key_rate_scale=key_rate_scale[j])
        current_features = [
            getattr(i, feature) for i in moving_melodic_features
        ]
        axes[j].plot(points, current_features)
        axes[j].set(xlabel='bar')
        if feature == 'key_rate':
            axes[j].set(
                ylabel=f'{feature} ({key_rate_scale[j].get_scale_name()})')
        else:
            axes[j].set(ylabel=feature)
        x_major_locator = plt.MultipleLocator(plot_bar_ticks)
        axes[j].xaxis.set_major_locator(x_major_locator)

    plt.show()


if __name__ == '__main__':
    midi_path = r'G:\music project files\mp3 and midi files\midi files'
    current_file = r'G:\music project files\mp3 and midi files\midi files\牧羊人的眼泪（又名沉睡国度）xin.mid'
    test_plot_multiple_moving_melodic_features(current_file,
                                               current_width=4,
                                               current_bar_interval=1 / 4,
                                               plot_bar_ticks=2,
                                               features=[
                                                   'pitch_mean', 'pitch_var',
                                                   'pitch_interval_mean',
                                                   'pitch_interval_var'
                                               ])
