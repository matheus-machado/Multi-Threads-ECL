#include <iostream>
#include <vector>
#include <thread>

using namespace std;

// Function to merge two sorted arrays
void merge(vector<int>& arr, int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    // Create temporary arrays
    vector<int> L(n1), R(n2);

    // Copy data to temporary arrays L[] and R[]
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    // Merge the temporary arrays back into arr[l..r]
    i = 0; // Initial index of first subarray
    j = 0; // Initial index of second subarray
    k = l; // Initial index of merged subarray
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        }
        else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of L[], if there are any
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copy the remaining elements of R[], if there are any
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

// Function to perform merge sort using multiple threads
void mergeSort(vector<int>& arr, int l, int r, int threads) {
    if (l < r) {
        int m = l + (r - l) / 2;

        // If the number of threads is greater than 1, split the work into two threads
        if (threads > 1) {
            // Create two threads
            thread t1(mergeSort, ref(arr), l, m, threads / 2);
            thread t2(mergeSort, ref(arr), m + 1, r, threads / 2);

            // Wait for the two threads to finish
            t1.join();
            t2.join();
        }
        else { // Otherwise, do the work sequentially
            mergeSort(arr, l, m, 1);
            mergeSort(arr, m + 1, r, 1);
        }

        // Merge the two sorted halves
        merge(arr, l, m, r);
    }
}

int main() {
    vector<int> arr = { 5, 3, 8, 6, 2, 7, 1, 4 };
    int n = arr.size();
    int threads = 4;

    // Call mergeSort function with multiple threads
    mergeSort(arr, 0, n - 1, threads);

    // Print the sorted array
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}
