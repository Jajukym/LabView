# coding=utf-8


def percentile(numbers: list, percent: float):
    """
    Find the percentile of a list of values.
    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @return - the percentile of the values
    """
    if not numbers:
        return None
    k = (len(numbers) - 1) * percent
    f = int(k)                          # floor function
    c = f + 1 if k > f else f      # ceiling function
    if f == c:
        return numbers[f]  # Exact value.
    d0 = numbers[f]
    d1 = numbers[c]
    return (d0 + d1) / 2  # Proper hinge value.


starttime = time.perf_counter()
script_update("Starting Many_Many_Messages")

test_value = 0
maxtime = 0
total_time = 0
number_of_numbers = 100000
all_times = list(range(number_of_numbers))

for i in range(number_of_numbers):
    internaltime = time.perf_counter()
    test_value = x_LabVIEW_test(str(i))
    dmmtime = time.perf_counter() - internaltime
    all_times[i] = dmmtime
    total_time += dmmtime
    avgtime = total_time / (i + 1)
    if dmmtime > maxtime:
        maxtime = dmmtime
    script_update(str(i) + ': MaxTime: {:.3f}'.format(maxtime) +
        " Test Value - " + str(test_value) +
        '  LabVIEW Response Time: {:.3f}'.format(dmmtime) +
        '  Average: {:.3f}'.format(avgtime))

elapsed = time.perf_counter() - starttime
script_update("Time elapsed: " + str(elapsed))

all_times.sort(key=float)
all_times_min = min(all_times)
all_times_Q1 = percentile(all_times, 0.25)
all_times_median = percentile(all_times, 0.5)
all_times_Q3 = percentile(all_times, 0.75)
all_times_max = max(all_times)
script_update("The five-number summary of the data is: " +
              str(all_times_min) + ", " +
              str(all_times_Q1) + ", " +
              str(all_times_median) + ", " +
              str(all_times_Q3) + ", " +
              str(all_times_max))
script_update("The number of times greater than 10 ms is " +
              str(sum(i > 0.01 for i in all_times)))
script_update("The number of times greater than 5 ms is " +
              str(sum(i > 0.005 for i in all_times)))
iqr = all_times_Q3 - all_times_Q1
high_end_outlier = all_times_Q3 + 1.5 * iqr
low_end_outlier = all_times_Q1 - 1.5 * iqr

index = number_of_numbers - 1
while all_times[index] > high_end_outlier:
    index -= 1
script_update("The number of outliers on the high end is " +
              str(number_of_numbers - 1 - index))

index = 0
while all_times[index] < low_end_outlier:
    index += 1
script_update("The number of outliers on the low end is " +
              str(index))

