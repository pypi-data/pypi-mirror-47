#pragma once
#include <string>
#include <cmath>
#include <random>
#include <vector>
#include <limits>
#include <algorithm>


namespace RNG {
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
        auto const width = Integer { std::abs(step) + std::abs(start - stop) - 1 };
        return std::min(start, stop) + step * random_index(width / step);
    }

    /// RNG
    auto bernoulli(Float truth_factor) -> bool {
        auto distribution = std::bernoulli_distribution {
            smart_clamp(truth_factor, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto binomial(Integer number_of_trials, Float probability) -> Integer {
        auto distribution = std::binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto negative_binomial(Integer number_of_trials, Float probability) -> Integer {
        auto distribution = std::negative_binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto geometric(Float probability) -> Integer {
        auto distribution = std::geometric_distribution<Integer> { smart_clamp(probability, 0.0, 1.0) };
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

} // end namespace
