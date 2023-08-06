#pragma once
#include <algorithm>
#include <cmath>
#include <limits>
#include <random>
#include <vector>


namespace Fortuna {
    using Integer = long long;
    using Float = double;

    static std::random_device hardware_seed;
    static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256> hurricane {hardware_seed()};

    Integer min_int() { return -std::numeric_limits<Integer>::max(); }
    Integer max_int() { return std::numeric_limits<Integer>::max(); }
    Float min_float() { return std::numeric_limits<Float>::lowest(); }
    Float max_float() { return std::numeric_limits<Float>::max(); }
    Float min_below() { return std::nextafter(0.0, std::numeric_limits<Float>::lowest()); }
    Float min_above() { return std::nextafter(0.0, std::numeric_limits<Float>::max()); }

    template <typename Number>
    Number smart_clamp(Number target, Number left_limit, Number right_limit) {
        return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
    }

    template <typename Function, typename Number, typename Offset>
    Number analytic_continuation(Function && func, Number number, Offset offset) {
        if (number > 0) return func(number);
        if (number < 0) return -func(-number) + offset;
        return offset;
    }

    Float generate_canonical() {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(hurricane);
    }

    Float random_float(Float left_limit, Float right_limit) {
        std::uniform_real_distribution<Float> distribution { left_limit, right_limit };
        return distribution(hurricane);
    }

    Integer random_below(Integer number) {
        if (number > 0) {
            std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
            return distribution(hurricane);
        }
        return analytic_continuation(random_below, number, 0);
    }

    Integer random_index(Integer number) {
        if (number > 0) {
            std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
            return distribution(hurricane);
        }
        return analytic_continuation(random_index, number, -1);
    }

    Integer random_int(Integer left_limit, Integer right_limit) {
        std::uniform_int_distribution<Integer> distribution {
            std::min(left_limit, right_limit),
            std::max(left_limit, right_limit),
        };
        return distribution(hurricane);
    }

    Integer random_range(Integer start, Integer stop, Integer step) {
        if (start == stop or step == 0) return start;
        const auto width { std::abs(start - stop) - 1 };
        const auto pivot { step > 0 ? std::min(start, stop) : std::max(start, stop) };
        const auto step_size { std::abs(step) };
        return pivot + step_size * random_below((width + step_size) / step);
    }

    /// RNG
    bool bernoulli(double truth_factor) {
        std::bernoulli_distribution distribution {
            std::clamp(truth_factor, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    Integer binomial(Integer number_of_trials, double probability) {
        std::binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0),
        };
        return distribution(hurricane);
    }

    Integer negative_binomial(Integer number_of_trials, double probability) {
        std::negative_binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    Integer geometric(double probability) {
        std::geometric_distribution<Integer> distribution { std::clamp(probability, 0.0, 1.0) };
        return distribution(hurricane);
    }

    Integer poisson(double mean) {
        std::poisson_distribution<Integer> distribution { mean };
        return distribution(hurricane);
    }

    Float expovariate(Float lambda_rate) {
        std::exponential_distribution<Float> distribution { lambda_rate };
        return distribution(hurricane);
    }

    Float gammavariate(Float shape, Float scale) {
        std::gamma_distribution<Float> distribution { shape, scale };
        return distribution(hurricane);
    }

    Float weibullvariate(Float shape, Float scale) {
        std::weibull_distribution<Float> distribution { shape, scale };
        return distribution(hurricane);
    }

    Float normalvariate(Float mean, Float std_dev) {
        std::normal_distribution<Float> distribution { mean, std_dev };
        return distribution(hurricane);
    }

    Float lognormvariate(Float log_mean, Float log_deviation) {
        std::lognormal_distribution<Float> distribution { log_mean, log_deviation };
        return distribution(hurricane);
    }

    Float extreme_value(Float location, Float scale) {
        std::extreme_value_distribution<Float> distribution { location, scale };
        return distribution(hurricane);
    }

    Float chi_squared(Float degrees_of_freedom) {
        std::chi_squared_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(hurricane);
    }

    Float cauchy(Float location, Float scale) {
        std::cauchy_distribution<Float> distribution { location, scale };
        return distribution(hurricane);
    }

    Float fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) {
        std::fisher_f_distribution<Float> distribution {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return distribution(hurricane);
    }

    Float student_t(Float degrees_of_freedom) {
        std::student_t_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(hurricane);
    }

    /// Pyewacket
    Float betavariate(Float alpha, Float beta) {
        const auto y { gammavariate(alpha, 1.0) };
        if (y == 0) return 0.0;
        return y / (y + gammavariate(beta, 1.0));
    }

    Float paretovariate(Float alpha) {
        const auto u { 1.0 - generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }

    Float vonmisesvariate(Float mu, Float kappa) {
        static const auto PI { 4 * std::atan(1) };
        static const auto TAU { 8 * std::atan(1) };
        if (kappa <= 0.000001) return TAU * generate_canonical();
            const auto s { 0.5 / kappa };
            const auto r { s + std::sqrt(1 + s * s) };
            auto u1 {0};
            auto z {0};
            auto d {0};
            auto u2 {0};
            while (true) {
                u1 = generate_canonical();
                z = std::cos(PI * u1);
                d = z / (r + z);
                u2 = generate_canonical();
                if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
            }
        const auto q { 1.0 / r };
        const auto f { (q + z) / (1.0 + q * z) };
        const auto u3 { generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        return std::fmod(mu - std::acos(f), TAU);
    }

    Float triangular(Float low, Float high, Float mode) {
        if (high - low == 0) return low;
        auto u { generate_canonical() };
        auto c { (mode - low) / (high - low) };
        if (u > c) {
            u = 1.0 - u;
            c = 1.0 - c;
            const auto temp = low;
            low = high;
            high = temp;
        }
        return low + (high - low) * std::sqrt(u * c);
    }

    /// Fortuna
    bool percent_true(Float truth_factor) {
        return random_float(0.0, 100.0) < truth_factor;
    }

    template<typename Int>
    auto d(Int sides) -> Int {
        if (sides > 0) {
            std::uniform_int_distribution<Int> distribution {1, sides};
            return distribution(hurricane);
        }
        return analytic_continuation(d<Int>, sides, 0);
    }

    template<typename Int>
    auto dice(Int rolls, Int sides) -> Int {
        if (rolls > 0) {
            auto total {0};
            for (auto i {0}; i < rolls; ++i)
                total += d(sides);
            return total;
        }
        return analytic_continuation([sides](auto r){ return dice<Int>(r, sides); }, rolls, 0);
    }

    int ability_dice(int number) {
        const int num { std::clamp(number, 3, 9) };
        if (num == 3) return dice(3, 6);
        std::vector<int> theRolls(num);
        auto start = begin(theRolls);
        auto pivot = start + 3;
        auto stop = end(theRolls);
        std::generate_n(start, num, []() { return d(6); });
        std::partial_sort(start, pivot, stop, std::greater<>());
        return std::reduce(start, pivot);
    }

    Integer plus_or_minus(Integer number) {
        return random_int(-number, number);
    }

    Integer plus_or_minus_linear(Integer number) {
        const auto num { std::abs(number) };
        return dice<Integer>(2, num + 1) - (num + 2);
    }

    Integer plus_or_minus_gauss(Integer number) {
        static const auto PI { 4 * std::atan(1) };
        const auto num { std::abs(number) };
        const auto result { Integer(std::round(normalvariate(0.0, num / PI))) };
        if (result >= -num and result <= num) return result;
        return plus_or_minus_linear(num);
    }

    Integer fuzzy_clamp(Integer target, Integer upper_bound) {
        if (target >= 0 and target < upper_bound) return target;
        return random_index(upper_bound);
    }

    /// ZeroCool Methods
    Integer back_gauss(Integer);
    Integer front_gauss(Integer number) {
        if (number > 0) {
            const auto result { Integer(gammavariate(1.0, number / 10.0)) };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(back_gauss, number, -1);
    }

    Integer middle_gauss(Integer number) {
        if (number > 0) {
            const auto result { Integer(std::floor(normalvariate(number / 2.0, number / 10.0))) };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(middle_gauss, number, -1);
    }

    Integer back_gauss(Integer number) {
        if (number > 0) {
            return number - front_gauss(number) - 1;
        }
        return analytic_continuation(front_gauss, number, -1);
    }

    Integer quantum_gauss(Integer number) {
        const auto rand_num { d(3) };
        if (rand_num == 1) return front_gauss(number);
        if (rand_num == 2) return middle_gauss(number);
        return back_gauss(number);
    }

    Integer back_poisson(Integer);
    Integer front_poisson(Integer number) {
        if (number > 0) {
            const auto result { poisson(number / 4.0) };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(back_poisson, number, -1);
    }

    Integer back_poisson(Integer number) {
        if (number > 0) {
            const auto result { number - front_poisson(number) - 1 };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(front_poisson, number, -1);
    }

    Integer middle_poisson(Integer number) {
        if (percent_true(50)) return front_poisson(number);
        return back_poisson(number);
    }

    Integer quantum_poisson(Integer number) {
        const auto rand_num { d(3) };
        if (rand_num == 1) return front_poisson(number);
        if (rand_num == 2) return middle_poisson(number);
        return back_poisson(number);
    }

    Integer back_linear(Integer);
    Integer front_linear(Integer number) {
        if (number > 0) {
            return triangular(0, number, 0);
        }
        return analytic_continuation(back_linear, number, -1);
    }

    Integer back_linear(Integer number) {
        if (number > 0) {
            return triangular(0, number, number);
        }
        return analytic_continuation(front_linear, number, -1);
    }

    Integer middle_linear(Integer number) {
        if (number > 0) {
            return triangular(0, number, number / 2.0);
        }
        return analytic_continuation(middle_linear, number, -1);
    }

    Integer quantum_linear(Integer number) {
        const auto rand_num { d(3) };
        if (rand_num == 1) return front_linear(number);
        if (rand_num == 2) return middle_linear(number);
        return back_linear(number);
    }

    Integer quantum_monty(Integer number) {
        const auto rand_num { d(3) };
        if (rand_num == 1) return quantum_linear(number);
        if (rand_num == 2) return quantum_gauss(number);
        return quantum_poisson(number);
    }

    /// Generators
    template<typename Value>
    Value random_value(const std::vector<Value> & data) {
        return data[Fortuna::random_index(data.size())];
    }

    template<typename Value, typename ZeroCool>
    Value random_value(const std::vector<Value> & data, ZeroCool && func) {
        return data[func(data.size())];
    }

    template<typename Value, typename Function>
    Value random_rotate(std::vector<Value> & values, Function && func, size_t range_to) {
        auto pivot { begin(values) + 1 + func(range_to) };
        return * std::rotate(begin(values), pivot, end(values));
    }

    template<typename Value, typename Function>
    Value random_rotate(std::vector<Value> & values, Function && func) {
        return Fortuna::random_rotate(values, func, values.size() - 1);
    }

    template<typename Value>
    Value random_rotate(std::vector<Value> & values) {
        return Fortuna::random_rotate(values, Fortuna::front_poisson);
    }

    template<typename Value>
    struct TruffleShuffle {
        std::vector<Value> values;
        TruffleShuffle(std::vector<Value> values) : values(values) {
            std::shuffle(begin(values), end(values), Fortuna::hurricane);
        }
        Value operator()() {
            if (values.size() == 1) return values.front();
            return Fortuna::random_rotate(values);
        }
    };

    template<typename Weight>
    std::vector<Weight> cumulative_from_relative(const std::vector<Weight> & rel_weights) {
        std::vector<Weight> cum_weights(rel_weights.size());
        std::partial_sum(begin(rel_weights), end(rel_weights), begin(cum_weights));
        return cum_weights;
    }

    template<typename Weight>
    std::vector<Weight> relative_from_cumulative(const std::vector<Weight> & cum_weights) {
        std::vector<Weight> rel_weights(cum_weights.size());
        std::adjacent_difference(begin(cum_weights), end(cum_weights), begin(rel_weights));
        return rel_weights;
    }

    template<typename Weight, typename Value>
    Value cumulative_weighted_choice(const std::vector<Weight> & weights, const std::vector<Value> & values) {
        const auto max_weight { weights.back() };
        const auto raw_weight { Fortuna::random_float(0.0, max_weight) };
        const auto valid_weight { std::lower_bound(begin(weights), end(weights), raw_weight) };
        const auto result_idx { std::distance(begin(weights), valid_weight) };
        return values[result_idx];
    }

} // end Fortuna namespace
