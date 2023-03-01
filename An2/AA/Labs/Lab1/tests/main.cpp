#include <bits/stdc++.h>

using namespace std;

long long get_det(pair<long long, long long> p, pair<long long, long long> q, pair<long long, long long> r) {
    return q.first * r.second + r.first * p.second + p.first * q.second - p.second * q.first - q.second * r.first - r.second * p.first;
}

void get_hull(list<int> &hull, vector<pair<long long, long long>> &points)
{
    hull.push_back(0);
    hull.push_back(1);

    for (int i = 2; i < points.size(); ++i) {
        while (hull.size() >= 2) {
            auto it = hull.end();
            int llast = *(--(--it));
            int last = *(++it);

            long long det = get_det(points[llast], points[last], points[i]);
            if (det <= 0) {
                hull.pop_back();
            } else {
                break;
            }
        }
        hull.push_back(i);
    }

    hull.push_back(points.size() - 2);
    int mx = hull.size();

    for (int i = points.size() - 3; i >= 0; --i) {
        while (hull.size() >= mx) {
            auto it = hull.end();
            int llast = *(--(--it));
            int last = *(++it);

            long long det = get_det(points[llast], points[last], points[i]);
            if (det <= 0) {
                hull.pop_back();
            } else {
                break;
            }
        }
        hull.push_back(i);
    }
}

double get_dist(vector<pair<long long, long long>> points, int p, list<int>::iterator d) {
    int it1, it2;
    it1 = *d;
    --d;
    it2 = *d;
    ++d;

    double dist1 = sqrt(pow(points[p].first - points[it1].first, 2) + pow(points[p].second - points[it1].second, 2));
    double dist2 = sqrt(pow(points[p].first - points[it2].first, 2) + pow(points[p].second - points[it2].second, 2));
    double dist3 = sqrt(pow(points[it1].first - points[it2].first, 2) + pow(points[it1].second - points[it2].second, 2));
    return dist1 + dist2 - dist3;
}

double get_rate(vector<pair<long long, long long>> points, int p, list<int>::iterator d) {
    int it1, it2;
    it1 = *d;
    --d;
    it2 = *d;
    ++d;

    double dist1 = sqrt(pow(points[p].first - points[it1].first, 2) + pow(points[p].second - points[it1].second, 2));
    double dist2 = sqrt(pow(points[p].first - points[it2].first, 2) + pow(points[p].second - points[it2].second, 2));
    double dist3 = sqrt(pow(points[it1].first - points[it2].first, 2) + pow(points[it1].second - points[it2].second, 2));
    return (dist1 + dist2) / dist3;
}

void get_sol(list<int> &hull, vector<pair<long long, long long>> points)
{
    vector<bool> added(points.size(), false);
    for (auto it:hull) {
        added[it] = true;
    }

    vector<list<int>::iterator> mn(points.size(), hull.begin());

    for (int i = 0; i < points.size(); ++i) {
        if (added[i]) {
            continue;
        }

        list<int>::iterator it = hull.begin();
        ++(++it);

        ++(mn[i]);

        while (it != hull.end()) {
            if (get_dist(points, i, it) < get_dist(points, i, mn[i])) {
                mn[i] = it;
            }

            ++it;
        }
    }

    while (hull.size() <= points.size()) {
        int mnind = -1;
        for (int i = 0; i < points.size(); ++i) {
            if (added[i]) {
                continue;
            }

            if (mnind == -1 || get_rate(points, i, mn[i]) < get_rate(points, mnind, mn[mnind])) {
                mnind = i;
            }
        }

        added[mnind] = true;
        hull.insert(mn[mnind], mnind);

        for (int i = 0; i < points.size(); ++i) {
            if (added[i]) {
                continue;
            }

            list<int>::iterator it = mn[mnind];
            if (get_dist(points, i, it) < get_dist(points, i, mn[i])) {
                mn[i] = it;
            }

            --it;
            if (get_dist(points, i, it) < get_dist(points, i, mn[i])) {
                mn[i] = it;
            }
        }
    }
}

int main() {
    int n;
    cin >> n;

    vector<pair<long long, long long>> points;
    map<pair<long long, long long>, int> individuals;
    for (int i = 0; i < n; ++i) {
        int x, y;
        cin >> x >> y;
        individuals[make_pair(x, y)]++;
    }

    for (auto it:individuals) {
        points.push_back(it.first);
    }
    n = points.size();

    list<int> hull;
    get_hull(hull, points);

    get_sol(hull, points);

    for (auto pt:hull) {
        if (!individuals[points[pt]]) {
            cout << points[pt].first << " " << points[pt].second << "\n";
        }

        for (int i = 0; i < individuals[points[pt]]; ++i) {
            cout << points[pt].first << " " << points[pt].second << "\n";
        }
        individuals[points[pt]] = 0;
    }

    return 0;
}
