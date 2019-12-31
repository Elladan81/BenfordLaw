import sys
import math
from _collections import defaultdict
import matplotlib.pyplot as plt

# Benford's law percentages for the first digits (1-9)
BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]


def load_data(filename):
    """import data form a file"""
    with open(filename) as f:
        return f.read().strip().split('\n')


def count_first_digits(data_list):
    first_digits = defaultdict(int)
    for sample in data_list:
        if sample == '':
            continue
        try:
            int(sample)
        except ValueError as e:
            print(e, file=sys.stderr)
            print("Samples must be integer. Exiting.", file=sys.stderr)
            sys.exit(1)
        first_digits[sample[0]] += 1
    data_count = [v for (k, v) in sorted(first_digits.items())]
    total_count = sum(data_count)
    data_pct = [(i / total_count) * 100 for i in data_count]
    return data_count, data_pct, total_count


def get_expected_counts(total_count):
    return [round(p * total_count / 100) for p in BENFORD]


def chi_square_test(data_count, expected_counts):
    chi_square_stat = 0
    for data, expected in zip(data_count, expected_counts):
        chi_square = math.pow(data - expected, 2)
        chi_square_stat += chi_square / expected
    print("\nChi Squared Test Statistic = {:.3f}".format(chi_square_stat))
    print("Critical Value at a P_value of 0.05 is 15.51 ")

    return chi_square_stat < 15.51


def bar_chart(data_pct):
    fig, ax = plt.subplots()

    index = [i + 1 for i in range(len(data_pct))]

    fig.canvas.set_window_title('percentage first digits')
    ax.set_title('Data vs Benford Values', fontsize=15)
    ax.set_ylabel('Frequency %', fontsize=16)
    ax.set_xticks(index)
    ax.set_xticklabels(index, fontsize=14)

    # build bars
    rects = ax.bar(index, data_pct, width=0.95, color='black', label='Data')

    # attach a text label on each bar displaying its height
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, '{:0.1f}'.format(height), ha='center', va='bottom',
                fontsize=13)

    # plot benford values as red dots
    ax.scatter(index, BENFORD, s=150, c='red', zorder=2, label='BENFORD')
    # hide right and top spine and add legend
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(prop={'size': 15}, frameon=False)

    plt.show()


def main():
    """call function and print stats"""
    # load data
    while True:
        filename = input("\n Name the file with COUNT data: ")
        try:
            data_list = load_data(filename)
        except IOError as e:
            print("{}. Try again.".format(e), file=sys.stderr)

        else:
            break

    data_count, data_pct, total_count = count_first_digits(data_list)
    expected_counts = get_expected_counts(total_count)
    print("\nobserved counts = {}".format(data_count))
    print("expected counts = {}".format(expected_counts))

    print("First Digit Probabilites:")
    for i in range(1, 10):
        print("{}:observed: {:.3f} expected {:.3f}".format(i, data_pct[i - 1] / 100, BENFORD[i - 1] / 100))

    if chi_square_test(data_count, expected_counts):
        print("Observed distribution matches expected distribution")
    else:
        print("Observed distribution does not match expected distribution.", file=sys.stderr)

    bar_chart(data_pct)


if __name__ == '__main__':
    main()
