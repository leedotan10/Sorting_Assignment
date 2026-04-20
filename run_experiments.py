import argparse
import random
import time
import statistics
import sys
import matplotlib.pyplot as plt

SORT_NAMES = {
    3: "Insertion Sort",
    4: "Merge Sort",
    5: "Quick Sort"
}


def insertion_sort(arr):
    nums = arr[:]
    for i in range(1, len(nums)):
        current = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > current:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = current
    return nums


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    middle = len(arr) // 2
    left_part = merge_sort(arr[:middle])
    right_part = merge_sort(arr[middle:])
    return merge_lists(left_part, right_part)


def merge_lists(left, right):
    answer = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            answer.append(left[i])
            i += 1
        else:
            answer.append(right[j])
            j += 1

    while i < len(left):
        answer.append(left[i])
        i += 1

    while j < len(right):
        answer.append(right[j])
        j += 1

    return answer


def quick_sort(arr):
    nums = arr[:]
    quick_sort_rec(nums, 0, len(nums) - 1)
    return nums


def quick_sort_rec(nums, low, high):
    if low < high:
        p = split(nums, low, high)
        quick_sort_rec(nums, low, p - 1)
        quick_sort_rec(nums, p + 1, high)


def split(nums, low, high):
    pivot_idx = random.randint(low, high)
    nums[pivot_idx], nums[high] = nums[high], nums[pivot_idx]

    pivot = nums[high]
    i = low - 1

    for j in range(low, high):
        if nums[j] <= pivot:
            i += 1
            nums[i], nums[j] = nums[j], nums[i]

    nums[i + 1], nums[high] = nums[high], nums[i + 1]
    return i + 1


def get_sort_func(sort_id):
    if sort_id == 3:
        return insertion_sort
    if sort_id == 4:
        return merge_sort
    if sort_id == 5:
        return quick_sort
    raise ValueError("This submission supports only algorithms 3, 4, and 5.")


def make_random_array(n):
    return [random.randint(0, 1_000_000) for _ in range(n)]


def make_almost_sorted_array(n, noise_level):
    arr = list(range(n))
    swaps = max(1, int(n * noise_level))

    for _ in range(swaps):
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        arr[a], arr[b] = arr[b], arr[a]

    return arr


def check_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def time_sort(sort_func, arr):
    start = time.perf_counter()
    sorted_arr = sort_func(arr)
    end = time.perf_counter()

    if not check_sorted(sorted_arr):
        raise ValueError("Sorting result is incorrect")

    return end - start


def run_tests(sort_ids, sizes, reps, experiment_name, noise_level=0.0):
    all_results = {}

    for sort_id in sort_ids:
        name = SORT_NAMES[sort_id]
        func = get_sort_func(sort_id)

        all_results[name] = {
            "x": [],
            "avg": [],
            "std": []
        }

        for size in sizes:
            times = []

            for _ in range(reps):
                if experiment_name == "random":
                    arr = make_random_array(size)
                else:
                    arr = make_almost_sorted_array(size, noise_level)

                t = time_sort(func, arr)
                times.append(t)

            avg_time = statistics.mean(times)
            std_time = statistics.stdev(times) if len(times) > 1 else 0.0

            all_results[name]["x"].append(size)
            all_results[name]["avg"].append(avg_time)
            all_results[name]["std"].append(std_time)

            print(
                experiment_name,
                "|",
                name,
                "| size =",
                size,
                "| avg =",
                round(avg_time, 6),
                "| std =",
                round(std_time, 6)
            )

    return all_results


def draw_graph(results, title, file_name):
    plt.figure(figsize=(10, 6))

    for name, info in results.items():
        x_vals = info["x"]
        y_vals = info["avg"]
        std_vals = info["std"]

        plt.plot(x_vals, y_vals, marker="o", label=name)

        low_line = [max(0, y - s) for y, s in zip(y_vals, std_vals)]
        high_line = [y + s for y, s in zip(y_vals, std_vals)]
        plt.fill_between(x_vals, low_line, high_line, alpha=0.2)

    plt.title(title)
    plt.xlabel("Array size")
    plt.ylabel("Time in seconds")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()

    print("Saved:", file_name)


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", nargs="+", type=int, required=True)
    parser.add_argument("-s", nargs="+", type=int, required=True)
    parser.add_argument("-e", type=int, required=True, choices=[1, 2])
    parser.add_argument("-r", type=int, required=True)
    return parser.parse_args()


def main():
    random.seed(42)

    try:
        args = read_args()

        for alg in args.a:
            if alg not in [3, 4, 5]:
                raise ValueError("This submission supports only algorithms 3, 4, and 5.")

        for size in args.s:
            if size <= 0:
                raise ValueError("Array sizes must be positive")

        if args.r <= 0:
            raise ValueError("Repetitions must be positive")

        if args.e == 1:
            noise_level = 0.05
            result2_title = "Runtime on Nearly Sorted Arrays (5% noise)"
        else:
            noise_level = 0.20
            result2_title = "Runtime on Nearly Sorted Arrays (20% noise)"

        results_part_b = run_tests(
            sort_ids=args.a,
            sizes=args.s,
            reps=args.r,
            experiment_name="random"
        )

        draw_graph(
            results=results_part_b,
            title="Runtime on Random Arrays",
            file_name="result1.png"
        )

        results_part_c = run_tests(
            sort_ids=args.a,
            sizes=args.s,
            reps=args.r,
            experiment_name="noise",
            noise_level=noise_level
        )

        draw_graph(
            results=results_part_c,
            title=result2_title,
            file_name="result2.png"
        )

    except Exception as err:
        print("Error:", err)
        sys.exit(1)


if __name__ == "__main__":
    main()
