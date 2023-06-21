import sys

sys.path.append(r'G:\university\programming files\py files\musicpy\musicpy')
import musicpy as mp
import numpy as np


class Melody:

    def __init__(self, current_chord, filename=None, is_melody=False):
        if not is_melody:
            current_chord = mp.alg.split_melody(current_chord)
        self.current_chord = current_chord
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


q1 = mp.read(
    r'G:\music project files\mp3 and midi files\midi files\2023.1.9.mid')
q1 = q1.tracks[0]
q2 = mp.read(
    r'G:\music project files\mp3 and midi files\midi files\牧羊人的眼泪（又名沉睡国度）xin.mid'
)
q2 = q2.merge(get_off_drums=True)[0]
q2.clear_other_messages()
q2 = mp.alg.split_melody(q2)

m1 = Melody(q1)
m2 = Melody(q2)
