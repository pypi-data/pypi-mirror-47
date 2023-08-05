#pragma once
#include <string>
#include <cmath>
#include <random>
#include <vector>
#include <limits>
#include <algorithm>


namespace Fortuna {
    using Integer = long long;
    using Float = double;

    static std::random_device hardware_seed {};
    static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256> hurricane{hardware_seed()};

    auto min_int() -> Integer { return -std::numeric_limits<Integer>::max(); }
    auto max_int() -> Integer { return std::numeric_limits<Integer>::max(); }
    auto min_float() -> Float { return std::numeric_limits<Float>::lowest(); }
    auto max_float() -> Float { return std::numeric_limits<Float>::max(); }
    auto min_below() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::lowest()); }
    auto min_above() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::max()); }

    template <typename Number>
    auto smart_clamp(Number target, Number left_limit, Number right_limit) -> Number {
        return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
    }

    template <typename Function, typename Number, typename Size>
    auto analytic_continuation(Function && func, Number number, Size offset) -> Number {
        if (number > 0) return func(number);
        if (number < 0) return -func(-number) + offset;
        return offset;
    }

    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(hurricane);
    }

    auto random_float(Float left_limit, Float right_limit) -> Float {
        auto distribution = std::uniform_real_distribution<Float> { left_limit, right_limit };
        return distribution(hurricane);
    }

    auto random_below(Integer number) -> Integer {
        if (number > 0) {
            auto distribution = std::uniform_int_distribution<Integer> { 0, number - 1 };
            return distribution(hurricane);
        }
        return analytic_continuation(random_below, number, 0);
    }

    auto random_index(Integer number) -> Integer {
        if (number > 0) {
            auto distribution = std::uniform_int_distribution<Integer> { 0, number - 1 };
            return distribution(hurricane);
        }
        return analytic_continuation(random_index, number, -1);
    }

    auto random_int(Integer left_limit, Integer right_limit) -> Integer {
        auto distribution = std::uniform_int_distribution<Integer> {
            std::min(left_limit, right_limit),
            std::max(right_limit, left_limit)
        };
        return distribution(hurricane);
    }

    auto random_range(Integer start, Integer stop, Integer step) -> Integer {
        if (start == stop or step == 0) return start;
        const auto width = Integer { std::abs(step) + std::abs(start - stop) - 1 };
        return std::min(start, stop) + step * random_index(width / step);
    }

    /// RNG
    auto bernoulli(Float truth_factor) -> bool {
        auto distribution = std::bernoulli_distribution {
            std::clamp(truth_factor, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto binomial(Integer number_of_trials, Float probability) -> Integer {
        auto distribution = std::binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto negative_binomial(Integer number_of_trials, Float probability) -> Integer {
        auto distribution = std::negative_binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto geometric(Float probability) -> Integer {
        auto distribution = std::geometric_distribution<Integer> { std::clamp(probability, 0.0, 1.0) };
        return distribution(hurricane);
    }

    auto poisson(Float mean) -> Integer {
        auto distribution = std::poisson_distribution<Integer> { mean };
        return distribution(hurricane);
    }

    auto expovariate(Float lambda_rate) -> Float {
        auto distribution = std::exponential_distribution<Float> { lambda_rate };
        return distribution(hurricane);
    }

    auto gammavariate(Float shape, Float scale) -> Float {
        auto distribution = std::gamma_distribution<Float> { shape, scale };
        return distribution(hurricane);
    }

    auto weibullvariate(Float shape, Float scale) -> Float {
        auto distribution = std::weibull_distribution<Float> { shape, scale };
        return distribution(hurricane);
    }

    auto normalvariate(Float mean, Float std_dev) -> Float {
        auto distribution = std::normal_distribution<Float> { mean, std_dev };
        return distribution(hurricane);
    }

    auto lognormvariate(Float log_mean, Float log_deviation) -> Float {
        auto distribution = std::lognormal_distribution<Float> { log_mean, log_deviation };
        return distribution(hurricane);
    }

    auto extreme_value(Float location, Float scale) -> Float {
        auto distribution = std::extreme_value_distribution<Float> { location, scale };
        return distribution(hurricane);
    }

    auto chi_squared(Float degrees_of_freedom) -> Float {
        auto distribution = std::chi_squared_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return distribution(hurricane);
    }

    auto cauchy(Float location, Float scale) -> Float {
        auto distribution = std::cauchy_distribution<Float> { location, scale };
        return distribution(hurricane);
    }

    auto fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) -> Float {
        auto distribution = std::fisher_f_distribution<Float> {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return distribution(hurricane);
    }

    auto student_t(Float degrees_of_freedom) -> Float {
        auto distribution = std::student_t_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return distribution(hurricane);
    }

    /// Pyewacket
    auto betavariate(Float alpha, Float beta) -> Float {
        const auto y = Float { gammavariate(alpha, 1.0) };
        if (y == 0) return 0.0;
        return y / (y + gammavariate(beta, 1.0));
    }

    auto paretovariate(Float alpha) -> Float {
        const auto u = Float { 1.0 - generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }

    auto vonmisesvariate(Float mu, Float kappa) -> Float {
        static const auto PI = Float { 4 * std::atan(1) };
        static const auto TAU = Float { 2 * PI };
        if (kappa <= 0.000001) return TAU * generate_canonical();
            const auto s = Float { 0.5 / kappa };
            const auto r = Float { s + std::sqrt(1 + s * s) };
            auto u1 = Float {0};
            auto z = Float {0};
            auto d = Float {0};
            auto u2 = Float {0};
            while (true) {
                u1 = generate_canonical();
                z = std::cos(PI * u1);
                d = z / (r + z);
                u2 = generate_canonical();
                if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
            }
        const auto q = Float { 1.0 / r };
        const auto f = Float { (q + z) / (1.0 + q * z) };
        const auto u3 = Float { generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        return std::fmod(mu - std::acos(f), TAU);
    }

    auto triangular(Float low, Float high, Float mode) -> Float {
        if (high - low == 0) return low;
        auto u = Float { generate_canonical() };
        auto c = Float { (mode - low) / (high - low) };
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
    auto percent_true(Float truth_factor) -> bool {
        return random_float(0.0, 100.0) < truth_factor;
    }

    auto d(Integer sides) -> Integer {
        if (sides > 0) return random_int(1, sides);
        return analytic_continuation(d, sides, 0);
    }

    auto dice(Integer rolls, Integer sides) -> Integer {
        if (rolls > 0) {
            auto total = Integer {0};
            for (auto i {0}; i < rolls; ++i)
                total += d(sides);
            return total;
        }
        if (rolls == 0) return 0;
        return -dice(-rolls, sides);
    }

    auto ability_dice(Integer number) -> Integer {
        const auto num { std::clamp(number, Integer(3), Integer(9)) };
        if (num == 3) return dice(3, 6);
        std::vector<Integer> theRolls(num);
        std::generate(begin(theRolls), end(theRolls), []() { return d(6); });
        std::partial_sort(begin(theRolls), begin(theRolls) + 3, end(theRolls), std::greater<Integer>());
        return std::reduce(begin(theRolls), begin(theRolls) + 3);
    }

    auto plus_or_minus(Integer number) -> Integer {
        return random_int(-number, number);
    }

    auto plus_or_minus_linear(Integer number) -> Integer {
        const auto num { std::abs(number) };
        return dice(2, num + 1) - (num + 2);
    }

    auto plus_or_minus_gauss(Integer number) -> Integer {
        static const auto PI { 4 * std::atan(1) };
        const auto num { std::abs(number) };
        const Integer result = normalvariate(0.0, num / PI);
        if (result >= -num and result <= num) return result;
        return random_int(-num, num);
    }

    auto fuzzy_clamp(Integer target, Integer upper_bound) -> Integer {
        if (target >= 0 and target < upper_bound) return target;
        return random_index(upper_bound);
    }

    /// ZeroCool Methods
    auto front_gauss(Integer number) -> Integer;
    auto middle_gauss(Integer number) -> Integer;
    auto back_gauss(Integer number) -> Integer;
    auto quantum_gauss(Integer number) -> Integer;
    auto front_poisson(Integer number) -> Integer;
    auto middle_poisson(Integer number) -> Integer;
    auto back_poisson(Integer number) -> Integer;
    auto quantum_poisson(Integer number) -> Integer;
    auto front_linear(Integer number) -> Integer;
    auto middle_linear(Integer number) -> Integer;
    auto back_linear(Integer number) -> Integer;
    auto quantum_linear(Integer number) -> Integer;
    auto quantum_monty(Integer number) -> Integer;

    auto front_gauss(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Integer(gammavariate(1.0, number / 10.0)) };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(back_gauss, number, -1);
    }

    auto middle_gauss(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Integer(normalvariate(number / 2.0, number / 10.0)) };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(middle_gauss, number, -1);
    }

    auto back_gauss(Integer number) -> Integer {
        if (number > 0) {
            return number - front_gauss(number) - 1;
        }
        return analytic_continuation(front_gauss, number, -1);
    }

    auto quantum_gauss(Integer number) -> Integer {
        const auto rand_num { d(3) };
        if (rand_num == 1) return front_gauss(number);
        if (rand_num == 2) return middle_gauss(number);
        return back_gauss(number);
    }

    auto front_poisson(Integer number) -> Integer {
        if (number > 0) {
            const auto result { poisson(number / 4.0) };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(back_poisson, number, -1);
    }

    auto back_poisson(Integer number) -> Integer {
        if (number > 0) {
            const auto result { number - front_poisson(number) - 1 };
            return fuzzy_clamp(result, number);
        }
        return analytic_continuation(front_poisson, number, -1);
    }

    auto middle_poisson(Integer number) -> Integer {
        if (percent_true(50)) return front_poisson(number);
        return back_poisson(number);
    }

    auto quantum_poisson(Integer number) -> Integer {
        const auto rand_num { d(3) };
        if (rand_num == 1) return front_poisson(number);
        if (rand_num == 2) return middle_poisson(number);
        return back_poisson(number);
    }

    auto front_linear(Integer number) -> Integer {
        if (number > 0) {
            return triangular(0, number, 0);
        }
        return analytic_continuation(back_linear, number, -1);
    }

    auto back_linear(Integer number) -> Integer {
        if (number > 0) {
            return triangular(0, number, number);
        }
        return analytic_continuation(front_linear, number, -1);
    }

    auto middle_linear(Integer number) -> Integer {
        if (number > 0) {
            return triangular(0, number, number / 2.0);
        }
        return analytic_continuation(middle_linear, number, -1);
    }

    auto quantum_linear(Integer number) -> Integer {
        const auto rand_num { d(3) };
        if (rand_num == 1) return front_linear(number);
        if (rand_num == 2) return middle_linear(number);
        return back_linear(number);
    }

    auto quantum_monty(Integer number) -> Integer {
        const auto rand_num { d(3) };
        if (rand_num == 1) return quantum_linear(number);
        if (rand_num == 2) return quantum_gauss(number);
        return quantum_poisson(number);
    }

    /// Generators
    template<typename Value>
    auto random_value(const std::vector<Value> & data) -> Value {
        return data[Fortuna::random_index(data.size())];
    }

    template<typename Value, typename ZeroCool>
    auto random_value(const std::vector<Value> & data, ZeroCool && func) -> Value {
        return data[func(data.size())];
    }

    template<typename Value>
    class TruffleShuffle {
        std::vector<Value> data;
    public:
        TruffleShuffle(std::vector<Value> vec_of_values) : data(vec_of_values) {
            std::shuffle(begin(data), end(data), hurricane);
        }
        auto operator()() -> Value {
            const Value result = data.front();
            const auto start = begin(data);
            const auto stop = start + 1;
            const auto target = 1 + stop + Fortuna::back_poisson(data.size() - 1);
            std::rotate(start, stop, target);
            return result;
        }
    };

    template<typename Weight>
    auto cumulative_from_relative(std::vector<Weight> weights) -> std::vector<Weight> {
        std::partial_sum(begin(weights), end(weights), begin(weights));
        return weights;
    }

    template<typename Weight>
    auto relative_from_cumulative(std::vector<Weight> weights) -> std::vector<Weight> {
        std::adjacent_difference(begin(weights), end(weights), begin(weights));
        return weights;
    }

    template<typename Weight, typename Value>
    auto cumulative_weighted_choice(const std::vector<Weight> & weights, const std::vector<Value> & values) -> Value {
        const auto max_weight { weights.back() };
        const auto raw_weight { Fortuna::random_float(0.0, max_weight) };
        const auto valid_weight { std::lower_bound(begin(weights), end(weights), raw_weight) };
        const auto result_idx { std::distance(begin(weights), valid_weight) };
        return values[result_idx];
    }

} // end Fortuna namespace
