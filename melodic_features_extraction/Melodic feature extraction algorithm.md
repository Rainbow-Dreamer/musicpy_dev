# Melodic feature extraction algorithm

## Some eigenvalues of a melody are given the following definitions.

Given a set of notes with total number `n` and pitches `p1, p2, ... , pn ∈ N`, the bar intervals between the notes are `i1, i2, ... , in`, the bar length of the notes is `d1, d2, ... , dn`, and the absolute interval between each two adjacent notes is `pi1, pi2, . .pin`, where `pin = abs(p(n+1) - pn)`.

### Aspect of Note pitches

* The average of the note pitches `mean([p1, p2, ... , pn])` can reflect the approximate center of the overall melody range, but it is necessary to pre-process the notes by cleaning the upper and lower percentile to reduce the influence of possible exceptionally high or low melodies on the overall melody range.

* The variance of the pitch of the note `var([p1, p2, ... pn])` or standard deviation `std([p1, p2, ... pn])` can reflect how dramatically the overall melody fluctuates. Smaller values indicate that the melody changes less and is more stable, or that the melody is more in place, while larger values indicate that the melody is more likely to jump off, or that the melody is more likely to have larger changes in pitch over time (relative to the long term).

* The degree to which the pitch of a note fits the note name of a given scale (e.g. major or minor) can reflect the degree to which a melody conforms to the tonic. For example, given a scale `s = (pn1, pn2, pn3, pn4, pn5, pn6, pn7)`, where the scale is composed of note names, regardless of the number of octaves, the note names for calculating the pitch of a note (that is, the note names without looking at the number of octaves) `pn1, pn2, ... pnn` belongs to the scale `s` as a percentage of `len([i for i in pn if i in s]) / len(pn)`, the result is a decimal number between 0 and 1, the closer to 1 means that the melody fits the tonality of the given scale, the closer to 0 means that the melody deviates from the tonality of the given scale.

* The extreme difference `max(p) - min(p)` of the notes can reflect the breadth of the range involved in the melody and also the degree of concentration of the melody's range.

* The pitches of notes are cleaned by upper and lower percentile, and the very high and very low notes are removed. For the nine octaves from 0 to 8, the number of notes whose pitches fall within each octave is counted, and then the number of octaves is sorted from largest to smallest according to the number of occurrences of the notes' pitches, and then the number of occurrences is totalized starting from the octave with the highest number of occurrences, and if the number of notes currently totalized is greater than the total number of notes If the ratio of the number of notes currently accumulated to the total number of notes is greater than or equal to the note saturation threshold (e.g., 0.95), the number of octaves from the highest to the currently used octave is taken as the approximate range of the melody's distribution.

* The percentage of occurrences of each note name in the pitch of the note.

### Aspect of pitch intervals

* The average of the intervals of the notes `mean([pi1, pi2, ... , pin])`, which is the average interval of the overall melody, reflects the degree of variation of the overall melody. The smaller the value, the smaller the interval of the overall melody has been, the less likely it is to jump, while the larger the value, the larger the interval of the overall melody has been, the more often the melody jumps (relatively short-term).
* The variance of the intervals of notes `var([pi1, pi2, ... , pin])` or standard deviation `std([pi1, pi2, ... , pin])` can reflect the degree of variation in the intervals of the overall melody, with smaller values indicating that the melody's fluctuations have remained more stable or more jumpy, and larger values indicating that the melody's fluctuations tend to change over time.
* The proportion of occurrences of interval types of notes (e.g. major thirds, pure fifths) is also a measure of melodic similarity, calculating the percentage of occurrences of each type of interval in the intervals of the notes.

### Aspect of note intervals

* The variance or standard deviation of the note intervals reflects the degree of rhythmic variation of the melody, with smaller values indicating a simpler or more regular melody, and larger values indicating a more complex melody.

* The mean value of the intervals of notes after the upper and lower percentile cleaning can reflect the compactness of the melody's rhythm.

* The percentage of occurrence of the note intervals.

### Aspect of note lengths

* The variance or standard deviation of the note length reflects the degree of variation in the note length of the melody. A smaller value indicates a more fixed note length, a larger value indicates a greater variation in the note length, or perhaps the note length becomes more variable with the complexity of the rhythm. If the melody is not rhythmically complex, a larger value could indicate that the note length is more uncontrolled by the rhythm, or does not follow the rhythm, and is more independent of each other.

* The average of the note lengths after the upper and lower percentile cleaning reflects the compactness of the note lengths.

* The percentage of occurrences of the length of notes.

## Generate a statistically "high quality" melody by genetic algorithm

Given a target length n and a template melody m1, a melody m2 of length n is randomly generated by a genetic algorithm, whose "melodic quality" is close to that of m1.

The pitch of the notes can be chosen from a total of 88 notes from A0 - C8, the intervals of the notes can be chosen from 0, 1/(2^i) (1 <= i <= 4, i ∈ N) and their accompanying rhythms 1/(2^i) + 1/(2^(i+1)) (1 <= i <= 4, i ∈ N), and the length of the notes can be chosen from the selectable values of all non-zero note intervals.

The generated melody needs to achieve the following goals.

1. the variance or standard deviation of the note pitches of m2 needs to be close to that of m1, which allows the melody of m2 to fluctuate to a degree close to that of m1
2. if the tonality of m2 needs to match that of m1, the melody of m2 needs to be close to the tonality of m1 for the same scale; if it only needs m2 to match a certain tonality to the extent of m1, then the melody of m2 only needs to be close to m1 for the maximum of the set of scales it matches
3. the average of the note intervals of m2 needs to be close to that of m1, which allows the short-term fluctuation of the melody of m2 to be close to that of m1
4. the variance or standard deviation of the note intervals of m2 needs to be close to that of m1, which allows the short-term fluctuation of the melody of m2 to be close to that of m1
5. the variance or standard deviation of the note intervals of m2 needs to be close to that of m1, which allows the rhythmic complexity of the melody of m2 to be close to that of m1
6. the variance or standard deviation of the note length of m2 needs to be close to that of m1, so that the fluctuation of the length of the notes of m2 is close to that of m1
7. if the range of m2 itself needs to be close to that of m1, the approximate range of the pitch distribution of the notes of m2 needs to be close to that of m1
8. If the rhythmic compactness of m2 itself is to be similar to that of m1, then the average of the note intervals of m2 after upper and lower percentile cleaning needs to be close to that of m1, and the compactness of the note lengths needs to be similar
9. The extreme difference of notes can also be used as one of the indicators to measure the similarity of m2 and m1.

The pitch, note spacing, and note length of m2 can be trained separately, where each component corresponds to a variety of goals that need to be met simultaneously. The more goals that need to be met at the same time, and the higher the actual value of the goals required, the slower the iterative convergence of the genetic algorithm, requiring continuous attempts to adjust the training parameters in order to improve the quality of the training.

Before starting to run the algorithm, m1 needs to be pre-processed with data, and the pitch, note interval and note length of m1 will be cleaned in the upper and lower percentile to remove the outliers, where the pitch and note length are cleaned in the upper and lower 99th percentile, and the note interval is cleaned in the upper 99th percentile only, because the minimum value can go to 0, which is the case of notes played simultaneously.
