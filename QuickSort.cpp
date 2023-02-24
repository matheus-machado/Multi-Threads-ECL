#include <iostream>
#include <vector>
#include <thread>
#include <mutex>

std::mutex mtx;

void quicksort(std::vector<int>& arr, int left, int right) {
    if (left >= right) {
        return;
    }

    int pivot = arr[left + (right - left) / 2];
    int i = left;
    int j = right;

    while (i <= j) {
        while (arr[i] < pivot) {
            i++;
        }
        while (arr[j] > pivot) {
            j--;
        }

        if (i <= j) {
            std::swap(arr[i], arr[j]);
            i++;
            j--;
        }
    }

    std::thread t1, t2;
    if (left < j) {
        t1 = std::thread(quicksort, std::ref(arr), left, j);
    }
    if (i < right) {
        t2 = std::thread(quicksort, std::ref(arr), i, right);
    }

    if (t1.joinable()) {
        t1.join();
    }
    if (t2.joinable()) {
        t2.join();
    }
}

int main() {
    std::vector<int> arr = {4, 2, 1, 7, 8, 3, 5, 6};
    quicksort(arr, 0, arr.size() - 1);

    for (int i = 0; i < arr.size(); i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}