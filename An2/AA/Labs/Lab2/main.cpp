#include <bits/stdc++.h>

using namespace std;

struct point{
    long long x, y;
};

void solve_horizontal(const vector<point> &points) {
    long long mn = LLONG_MAX;
    int indmn = -1;
    for (int i = 0; i < points.size(); ++i) {
        if (points[i].x < mn) {
            mn = points[i].x;
            indmn = i;
        }
    }

    bool changed = false;
    for (int i = indmn; i != (indmn - 2 + points.size()) % points.size(); i = (i + 1) % points.size()) {
        int ind1 = i, ind2 = (i + 1) % points.size(), ind3 = (i + 2) % points.size();
        long long diff = (points[ind2].x - points[ind1].x) * (points[ind3].x - points[ind2].x);
        if (diff < 0) {
            if (changed) {
                cout << "NO\n";
                return;
            }
            changed = true;
        }
    }

    cout << "YES\n";

}

void solve_vertical(const vector<point> &points) {

    long long mn = LLONG_MAX;
    int indmn = -1;
    for (int i = 0; i < points.size(); ++i) {
        if (points[i].y < mn) {
            mn = points[i].y;
            indmn = i;
        }
    }

    bool changed = false;
    for (int i = indmn; i != (indmn - 2 + points.size()) % points.size(); i = (i + 1) % points.size()) {
        int ind1 = i, ind2 = (i + 1) % points.size(), ind3 = (i + 2) % points.size();
        long long diff = (points[ind2].y - points[ind1].y) * (points[ind3].y - points[ind2].y);
        if (diff < 0) {
            if (changed) {
                cout << "NO\n";
                return;
            }
            changed = true;
        }
    }

    cout << "YES\n";

}

int main() {
    int n;
    cin >> n;

    vector<point> points(n);
    for (auto &it:points) {
        cin >> it.x >> it.y;
    }

    solve_horizontal(points);
    solve_vertical(points);

    return 0;
}
