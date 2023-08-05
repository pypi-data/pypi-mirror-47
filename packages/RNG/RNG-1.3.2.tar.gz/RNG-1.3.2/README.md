# Random Number Generator: RNG Storm Engine

Python API for the C++ Random library.

**RNG is not suitable for cryptography, but it could be perfect for other random stuff like data science, experimental programming, A.I. and games.**


*Recommended Installation:* `$ pip install RNG`

Support this project: https://www.patreon.com/brokencode


Number Types, Precision & Size:
- Float: Python float -> double at the C++ layer.
    - Min Float: -1.7976931348623157e+308
    - Max Float:  1.7976931348623157e+308
    - Min Below Zero: -5e-324
    - Min Above Zero:  5e-324

- Integer: Python int -> long long at the C++ layer.
    - Input & Output Range: `(-2**63, 2**63)` or approximately +/- 9.2 billion billion.
    - Min Integer: -9223372036854775807
    - Max Integer:  9223372036854775807


#### Random Binary Function
- `bernoulli(ratio_of_truth: float) -> bool`
    - Bernoulli distribution.
    - @param ratio_of_truth :: the probability of True as a decimal. Expected input range: [0.0, 1.0], clamped.
    - @return :: True or False


#### Random Integer Functions
- `random_int(left_limit: int, right_limit: int) -> int`
    - Flat uniform distribution.
    - 20x faster than random.randint()
    - @param left_limit :: input A.
    - @param right_limit :: input B. 
    - @return :: random integer in the inclusive range [A, B] or [B, A] if B < A
- `random_below(upper_bound: int) -> int`
    - Flat uniform distribution.
    - @param upper_bound :: inout A
    - @return :: random integer in exclusive range [0, A) or (A, 0] if A < 0
- `binomial(number_of_trials: int, probability: float) -> int`
    - Based on the idea of flipping a coin and counting how many heads come up after some number of flips.
    - @param number_of_trials :: how many times to flip a coin.
    - @param probability :: how likely heads will be flipped. 0.5 is a fair coin. 1.0 is a double headed coin.
    - @return :: count of how many heads came up.
- `negative_binomial(trial_successes: int, probability: float) -> int`
    - Based on the idea of flipping a coin as long as it takes to succeed.
    - @param trial_successes :: the required number of heads flipped to succeed.
    - @param probability :: how likely heads will be flipped. 0.50 is a fair coin.
    - @return :: the count of how many tails came up before the required number of heads.
- `geometric(probability: float) -> int`
    - Same as random_negative_binomial(1, probability). 
- `poisson(mean: float) -> int`
    - @param mean :: sets the average output of the function.
    - @return :: random integer, poisson distribution centered on the mean.


#### Random Floating Point Functions
- `generate_canonical() -> float`
    - Evenly distributes real values of maximum precision.
    - @return :: random Float in range {0.0, 1.0} biclusive. The spec defines the output range to be [0.0, 1.0).
        - biclusive: feature/bug rendering the exclusivity of this function a bit more mysterious than desired. This is a known compiler bug.
- `random_float(left_limit: float, right_limit: float) -> float`
    - Suffers from the same biclusive feature/bug noted for generate_canonical().
    - @param left_limit :: input A 
    - @param right_limit :: input B
    - @return :: random Float in range {A, B} biclusive. The spec defines the output range to be [A, B).
- `normalvariate(mean: float, std_dev: float) -> float`
    - @param mean :: sets the average output of the function.
    - @param std_dev :: standard deviation. Specifies spread of data from the mean.
- `lognormvariate(log_mean: float, log_deviation: float) -> float`
    - @param log_mean :: sets the log of the mean of the function.
    - @param log_deviation :: log of the standard deviation. Specifies spread of data from the mean.
- `exponential(lambda_rate: float) -> float`
    - Produces random non-negative floating-point values, distributed according to probability density function.
    - @param lambda_rate :: λ constant rate of a random event per unit of time/distance.
    - @return :: The time/distance until the next random event. For example, this distribution describes the time between the clicks of a Geiger counter or the distance between point mutations in a DNA strand.
- `gammavariate(shape: float, scale: float) -> float`
    - Generalization of the exponential distribution.
    - Produces random positive floating-point values, distributed according to probability density function.    
    - @param shape :: α the number of independent exponentially distributed random variables.
    - @param scale :: β the scale factor or the mean of each of the distributed random variables.
    - @return :: the sum of α independent exponentially distributed random variables, each of which has a mean of β.
- `weibullvariate(shape: float, scale: float) -> float`
    - Generalization of the exponential distribution.
    - Similar to the gamma distribution but uses a closed form distribution function.
    - Popular in reliability and survival analysis.
- `extreme_value(location: float, scale: float) -> float`
    - Based on Extreme Value Theory. 
    - Used for statistical models of the magnitude of earthquakes and volcanoes.
- `chi_squared(degrees_of_freedom: float) -> float`
    - Used with the Chi Squared Test and Null Hypotheses to test if sample data fits an expected distribution.
- `cauchy(location: float, scale: float) -> float`
    - @param location :: It specifies the location of the peak. The default value is 0.0.
    - @param scale :: It represents the half-width at half-maximum. The default value is 1.0.
    - @return :: Continuous Distribution.
- `fisher_f(degrees_of_freedom_1: float, degrees_of_freedom_2: float) -> float`
    - F distributions often arise when comparing ratios of variances.
- `student_t(degrees_of_freedom: float) -> float`
    - T distribution. Same as a normal distribution except it uses the sample standard deviation rather than the population standard deviation.
    - As degrees_of_freedom goes to infinity it converges with the normal distribution.


#### Engines
- `mersenne_twister_engine`: internal only
    - Implements 64 bit Mersenne twister algorithm. Default engine on most systems.
- `linear_congruential_engine`: internal only
    - Implements linear congruential algorithm.
- `subtract_with_carry_engine`: internal only
    - Implements a subtract-with-carry (lagged Fibonacci) algorithm.
- `storm_engine`: internal only
    - RNG: Custom Engine
    - Default Standard


#### Engine Adaptors
Engine adaptors generate pseudo-random numbers using another random number engine as entropy source. They are generally used to alter the spectral characteristics of the underlying engine.
- `discard_block_engine`: internal only
    - Discards some output of a random number engine.
- `independent_bits_engine`: internal only
    - Packs the output of a random number engine into blocks of a specified number of bits.
- `shuffle_order_engine`: internal only
    - Delivers the output of a random number engine in a different order.


#### Seeds & Entropy Source
- `random_device`: internal only
    - Non-deterministic uniform random bit generator, although implementations are allowed to implement random_device using a pseudo-random number engine if there is no support for non-deterministic random number generation.
- `seed_seq`: internal only
    - General-purpose bias-eliminating scrambled seed sequence generator.


#### Distribution & Performance Test Suite
- `distribution_timer(func: staticmethod, *args, **kwargs) -> None`
    - For statistical analysis of non-deterministic numeric functions.
    - @param func :: Function method or lambda to analyze. `func(*args, **kwargs)`
    - @optional_kw num_cycles :: Total number of samples for distribution analysis.
    - @optional_kw post_processor :: Used to scale a large set of data into a smaller set of groupings.
- `quick_test(n=10000) -> None` 
    - Runs a battery of tests for every random distribution function in the module.
    - @param n :: the total number of samples to collect for each test. Default: 10,000


## Development Log
##### RNG 1.3.1
- Test Update

##### RNG 1.3.1
- Fixed Typos

##### RNG 1.3.0
- Storm Update

##### RNG 1.2.5
- Low level clean up

##### RNG 1.2.4
- Minor Typos Fixed

##### RNG 1.2.3
- Documentation Update
- Test Update
- Bug Fixes

##### RNG 1.0.0 - 1.2.2, internal
- API Changes:
    - randint changed to random_int
    - randbelow changed to random_below
    - random changed to generate_canonical
    - uniform changed to random_float

##### RNG 0.2.3
- Bug Fixes

##### RNG 0.2.2
- discrete() removed.

##### RNG 0.2.1
- minor typos
- discrete() depreciated.

##### RNG 0.2.0
- Major Rebuild.

##### RNG 0.1.22
- The RNG Storm Engine is now the default standard.
- Experimental Vortex Engine added for testing.

##### RNG 0.1.21 beta
- Small update to the testing suite.

##### RNG 0.1.20 beta
- Changed default inputs for random_int and random_below to sane values.
    - random_int(left_limit=1, right_limit=20) down from `-2**63, 2**63 - 1`
    - random_below(upper_bound=10) down from `2**63 - 1`

##### RNG 0.1.19 beta
- Broke some fixed typos, for a change of pace.

##### RNG 0.1.18 beta
- Fixed some typos.

##### RNG 0.1.17 beta
- Major Refactoring.
- New primary engine: Hurricane.
- Experimental engine Typhoon added: random_below() only.

##### RNG 0.1.16 beta
- Internal Engine Performance Tuning. 

##### RNG 0.1.15 beta
- Engine Testing.

##### RNG 0.1.14 beta
- Fixed a few typos.

##### RNG 0.1.13 beta
- Fixed a few typos.

##### RNG 0.1.12 beta
- Major Test Suite Upgrade.
- Major Bug Fixes.
    - Removed several 'foot-guns' in prep for fuzz testing in future releases.

##### RNG 0.1.11 beta
- Fixed small bug in the install script.

##### RNG 0.1.10 beta
- Fixed some typos.

##### RNG 0.1.9 beta
- Fixed some typos.

##### RNG 0.1.8 beta
- Fixed some typos.
- More documentation added.

##### RNG 0.1.7 beta
- The `random_floating_point` function renamed to `random_float`.
- The function `c_rand()` has been removed as well as all the cruft it required.
- Major Documentation Upgrade.
- Fixed an issue where keyword arguments would fail to propagate. Both, positional args and kwargs now work as intended.
- Added this Dev Log.

##### RNG 0.0.6 alpha
- Minor ABI changes.

##### RNG 0.0.5 alpha
- Tests redesigned slightly for Float functions.

##### RNG 0.0.4 alpha
- Random Float Functions Implemented.

##### RNG 0.0.3 alpha
- Random Integer Functions Implemented.

##### RNG 0.0.2 alpha
- Random Bool Function Implemented.

##### RNG 0.0.1 pre-alpha
- Planning & Design.


## Distribution and Performance Test Suite
```
Quick Test: RNG Storm Engine

Round Trip Numeric Limits:
 Min Integer: -9223372036854775808
 Max Integer:  9223372036854775807
 Min Float: -1.7976931348623157e+308
 Max Float:  1.7976931348623157e+308
 Min Below Zero: -5e-324
 Min Above Zero:  5e-324


Binary Tests

Output Analysis: bernoulli(0.3333333333333333)
Typical Timing: 63 ± 1 ns
Statistics of 1000 Samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.334
 Std Deviation: 0.47187568984497036
Distribution of 10000 Samples:
 False: 66.82%
 True: 33.18%


Integer Tests

Base Case
Output Analysis: Random.randint(1, 6)
Typical Timing: 1125 ± 11 ns
Statistics of 1000 Samples:
 Minimum: 1
 Median: 3
 Maximum: 6
 Mean: 3.494
 Std Deviation: 1.7154902817873692
Distribution of 10000 Samples:
 1: 16.75%
 2: 16.57%
 3: 16.09%
 4: 16.47%
 5: 17.27%
 6: 16.85%

Output Analysis: random_int(1, 6)
Typical Timing: 63 ± 1 ns
Statistics of 1000 Samples:
 Minimum: 1
 Median: 4
 Maximum: 6
 Mean: 3.513
 Std Deviation: 1.6872100277314848
Distribution of 10000 Samples:
 1: 16.5%
 2: 16.7%
 3: 16.81%
 4: 16.64%
 5: 16.28%
 6: 17.07%

Base Case
Output Analysis: Random.randrange(6)
Typical Timing: 813 ± 10 ns
Statistics of 1000 Samples:
 Minimum: 0
 Median: 2
 Maximum: 5
 Mean: 2.466
 Std Deviation: 1.7209897750439442
Distribution of 10000 Samples:
 0: 16.84%
 1: 16.34%
 2: 16.75%
 3: 16.76%
 4: 16.67%
 5: 16.64%

Output Analysis: random_below(6)
Typical Timing: 32 ± 3 ns
Statistics of 1000 Samples:
 Minimum: 0
 Median: 3
 Maximum: 5
 Mean: 2.507
 Std Deviation: 1.7300127005152142
Distribution of 10000 Samples:
 0: 16.65%
 1: 17.38%
 2: 16.21%
 3: 17.18%
 4: 16.46%
 5: 16.12%

Output Analysis: binomial(4, 0.5)
Typical Timing: 157 ± 6 ns
Statistics of 1000 Samples:
 Minimum: 0
 Median: 2
 Maximum: 4
 Mean: 2.02
 Std Deviation: 1.0259886220873273
Distribution of 10000 Samples:
 0: 6.23%
 1: 25.37%
 2: 37.35%
 3: 24.81%
 4: 6.24%

Output Analysis: negative_binomial(5, 0.75)
Typical Timing: 94 ± 4 ns
Statistics of 1000 Samples:
 Minimum: 0
 Median: 1
 Maximum: 8
 Mean: 1.649
 Std Deviation: 1.4859364074572663
Distribution of 10000 Samples:
 0: 23.98%
 1: 30.21%
 2: 21.79%
 3: 12.8%
 4: 6.52%
 5: 2.86%
 6: 1.15%
 7: 0.38%
 8: 0.21%
 9: 0.06%
 10: 0.03%
 11: 0.01%

Output Analysis: geometric(0.75)
Typical Timing: 63 ± 1 ns
Statistics of 1000 Samples:
 Minimum: 0
 Median: 0
 Maximum: 5
 Mean: 0.321
 Std Deviation: 0.6545130918380375
Distribution of 10000 Samples:
 0: 75.48%
 1: 18.74%
 2: 4.29%
 3: 1.07%
 4: 0.37%
 5: 0.05%

Output Analysis: poisson(4.5)
Typical Timing: 94 ± 8 ns
Statistics of 1000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 13
 Mean: 4.47
 Std Deviation: 2.1282926560108293
Distribution of 10000 Samples:
 0: 0.94%
 1: 5.21%
 2: 11.16%
 3: 16.82%
 4: 19.44%
 5: 16.87%
 6: 13.06%
 7: 8.14%
 8: 4.52%
 9: 2.27%
 10: 1.0%
 11: 0.33%
 12: 0.14%
 13: 0.07%
 14: 0.02%
 15: 0.01%


Floating Point Tests

Base Case
Output Analysis: Random.random()
Typical Timing: 32 ± 8 ns
Statistics of 1000 Samples:
 Minimum: 0.0018642861079508632
 Median: (0.4865522788422926, 0.48694668495861426)
 Maximum: 0.9985633134556822
 Mean: 0.48901738537454814
 Std Deviation: 0.28748684142665426
Post-processor Distribution of 10000 Samples using round method:
 0: 49.55%
 1: 50.45%

Output Analysis: generate_canonical()
Typical Timing: 32 ± 8 ns
Statistics of 1000 Samples:
 Minimum: 0.002359750132155993
 Median: (0.48431349416875374, 0.48573568810722473)
 Maximum: 0.9999435036254807
 Mean: 0.4943137436415561
 Std Deviation: 0.2900488178192246
Post-processor Distribution of 10000 Samples using round method:
 0: 51.21%
 1: 48.79%

Output Analysis: random_float(0.0, 10.0)
Typical Timing: 32 ± 8 ns
Statistics of 1000 Samples:
 Minimum: 0.004522243792486171
 Median: (4.921505459005925, 4.924210379552047)
 Maximum: 9.995787333576851
 Mean: 4.896222634165114
 Std Deviation: 2.916193866609588
Post-processor Distribution of 10000 Samples using floor method:
 0: 9.95%
 1: 10.21%
 2: 10.28%
 3: 9.7%
 4: 10.07%
 5: 10.16%
 6: 10.24%
 7: 10.04%
 8: 9.53%
 9: 9.82%

Base Case
Output Analysis: Random.expovariate(1.0)
Typical Timing: 313 ± 8 ns
Statistics of 1000 Samples:
 Minimum: 0.002216150797450532
 Median: (0.65490187439184, 0.6570304361976486)
 Maximum: 6.8602232620425925
 Mean: 0.9662768540796546
 Std Deviation: 0.9718578350843132
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.81%
 1: 23.15%
 2: 8.24%
 3: 3.1%
 4: 1.06%
 5: 0.45%
 6: 0.1%
 7: 0.07%
 8: 0.01%
 9: 0.01%

Output Analysis: expovariate(1.0)
Typical Timing: 32 ± 3 ns
Statistics of 1000 Samples:
 Minimum: 0.0001443232661739669
 Median: (0.604609619919764, 0.6058374269792876)
 Maximum: 7.523762627178045
 Mean: 0.950007897809117
 Std Deviation: 0.9903508341192871
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.47%
 1: 22.79%
 2: 8.69%
 3: 3.26%
 4: 1.1%
 5: 0.37%
 6: 0.2%
 7: 0.08%
 8: 0.02%
 9: 0.02%

Base Case
Output Analysis: Random.gammavariate(1.0, 1.0)
Typical Timing: 500 ± 6 ns
Statistics of 1000 Samples:
 Minimum: 0.0010388346856487658
 Median: (0.6843158205748362, 0.6844232963414119)
 Maximum: 7.0212957044378435
 Mean: 0.9905427667057285
 Std Deviation: 0.9861209526154319
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.15%
 1: 22.99%
 2: 8.74%
 3: 3.25%
 4: 1.27%
 5: 0.35%
 6: 0.17%
 7: 0.07%
 8: 0.01%

Output Analysis: gammavariate(1.0, 1.0)
Typical Timing: 63 ± 3 ns
Statistics of 1000 Samples:
 Minimum: 0.0005345626996068837
 Median: (0.6973929491715651, 0.700809651289934)
 Maximum: 6.895658731396534
 Mean: 0.992240907792841
 Std Deviation: 0.9685063029877555
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 62.5%
 1: 24.02%
 2: 8.59%
 3: 3.23%
 4: 1.08%
 5: 0.33%
 6: 0.16%
 7: 0.07%
 8: 0.01%
 9: 0.01%

Base Case
Output Analysis: Random.weibullvariate(1.0, 1.0)
Typical Timing: 407 ± 8 ns
Statistics of 1000 Samples:
 Minimum: 0.0005576390899240854
 Median: (0.7130756039405082, 0.7139022175371896)
 Maximum: 7.09116708798363
 Mean: 0.9649662155425063
 Std Deviation: 0.9043079942748469
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.1%
 1: 23.67%
 2: 8.82%
 3: 2.87%
 4: 0.86%
 5: 0.54%
 6: 0.08%
 7: 0.04%
 8: 0.02%

Output Analysis: weibullvariate(1.0, 1.0)
Typical Timing: 94 ± 6 ns
Statistics of 1000 Samples:
 Minimum: 0.0013769198506304672
 Median: (0.6854759401451815, 0.6860935612996812)
 Maximum: 6.334333188852022
 Mean: 0.9927655215478188
 Std Deviation: 0.9904626429090108
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 62.79%
 1: 23.72%
 2: 8.83%
 3: 3.09%
 4: 0.98%
 5: 0.4%
 6: 0.14%
 7: 0.03%
 8: 0.01%
 9: 0.01%

Output Analysis: extreme_value(0.0, 1.0)
Typical Timing: 63 ± 8 ns
Statistics of 1000 Samples:
 Minimum: -1.9168155334568997
 Median: (0.4202144360886349, 0.42021803685752834)
 Maximum: 7.534776672035387
 Mean: 0.6281455771570104
 Std Deviation: 1.2882972276403204
Post-processor Distribution of 10000 Samples using round method:
 -2: 1.16%
 -1: 17.89%
 0: 34.29%
 1: 26.1%
 2: 12.54%
 3: 4.94%
 4: 2.04%
 5: 0.76%
 6: 0.18%
 7: 0.08%
 8: 0.01%
 9: 0.01%

Base Case
Output Analysis: Random.gauss(5.0, 2.0)
Typical Timing: 563 ± 7 ns
Statistics of 1000 Samples:
 Minimum: -1.6634807888337688
 Median: (4.992411644420636, 4.999776377007621)
 Maximum: 11.690371059618943
 Mean: 5.010119985590884
 Std Deviation: 2.0205453733106298
Post-processor Distribution of 10000 Samples using round method:
 -3: 0.01%
 -2: 0.06%
 -1: 0.27%
 0: 1.06%
 1: 2.5%
 2: 6.61%
 3: 12.35%
 4: 17.78%
 5: 19.24%
 6: 17.32%
 7: 12.01%
 8: 6.64%
 9: 2.92%
 10: 0.93%
 11: 0.23%
 12: 0.06%
 13: 0.01%

Output Analysis: normalvariate(5.0, 2.0)
Typical Timing: 94 ± 1 ns
Statistics of 1000 Samples:
 Minimum: -0.4216081465400877
 Median: (4.957867873498797, 4.960525287092449)
 Maximum: 12.63349318909003
 Mean: 5.008923426162033
 Std Deviation: 1.9401326818290008
Post-processor Distribution of 10000 Samples using round method:
 -2: 0.05%
 -1: 0.21%
 0: 0.86%
 1: 2.78%
 2: 6.48%
 3: 12.26%
 4: 17.87%
 5: 19.34%
 6: 16.74%
 7: 12.33%
 8: 6.99%
 9: 2.7%
 10: 1.04%
 11: 0.28%
 12: 0.06%
 13: 0.01%

Base Case
Output Analysis: Random.lognormvariate(1.6, 0.25)
Typical Timing: 782 ± 23 ns
Statistics of 1000 Samples:
 Minimum: 2.100373404196032
 Median: (4.9760585202982925, 4.98628941430215)
 Maximum: 10.411691568142325
 Mean: 5.09383254093055
 Std Deviation: 1.2592170395705158
Post-processor Distribution of 10000 Samples using round method:
 2: 0.39%
 3: 7.53%
 4: 27.06%
 5: 31.19%
 6: 20.01%
 7: 8.56%
 8: 3.76%
 9: 0.97%
 10: 0.43%
 11: 0.07%
 12: 0.03%

Output Analysis: lognormvariate(1.6, 0.25)
Typical Timing: 94 ± 6 ns
Statistics of 1000 Samples:
 Minimum: 2.3102686193133475
 Median: (5.019794704716817, 5.022776860977586)
 Maximum: 12.469002534530496
 Mean: 5.11371929182671
 Std Deviation: 1.2248494106461876
Post-processor Distribution of 10000 Samples using round method:
 2: 0.18%
 3: 7.82%
 4: 26.79%
 5: 31.61%
 6: 19.92%
 7: 9.1%
 8: 3.08%
 9: 1.08%
 10: 0.3%
 11: 0.08%
 12: 0.04%

Output Analysis: chi_squared(1.0)
Typical Timing: 125 ± 5 ns
Statistics of 1000 Samples:
 Minimum: 3.085701168854021e-06
 Median: (0.48285661922698087, 0.48467165992763533)
 Maximum: 10.254473577411064
 Mean: 1.046383503767532
 Std Deviation: 1.4927844622805495
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 68.1%
 1: 16.17%
 2: 7.23%
 3: 3.74%
 4: 2.09%
 5: 1.14%
 6: 0.71%
 7: 0.44%
 8: 0.25%
 9: 0.13%

Output Analysis: cauchy(0.0, 1.0)
Typical Timing: 63 ± 8 ns
Statistics of 1000 Samples:
 Minimum: -732.5261850485788
 Median: (-0.020055265859094697, -0.017184836963910936)
 Maximum: 306.47288939150184
 Mean: -0.6510962692967972
 Std Deviation: 35.35932237331378
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 26.13%
 1: 11.46%
 2: 5.64%
 3: 3.76%
 4: 2.71%
 5: 3.2%
 6: 3.87%
 7: 6.02%
 8: 11.36%
 9: 25.85%

Output Analysis: fisher_f(8.0, 8.0)
Typical Timing: 188 ± 8 ns
Statistics of 1000 Samples:
 Minimum: 0.07352853206082759
 Median: (0.9890826680010241, 0.9912238450887711)
 Maximum: 31.86094635990357
 Mean: 1.3431530252093435
 Std Deviation: 1.4457616619997709
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 49.96%
 1: 32.66%
 2: 10.12%
 3: 3.72%
 4: 1.75%
 5: 0.81%
 6: 0.49%
 7: 0.25%
 8: 0.13%
 9: 0.11%

Output Analysis: student_t(8.0)
Typical Timing: 157 ± 7 ns
Statistics of 1000 Samples:
 Minimum: -7.716646203378542
 Median: (-0.019686697570107447, -0.01893513978694138)
 Maximum: 5.106134947613407
 Mean: -0.05970990825645788
 Std Deviation: 1.16938035996734
Post-processor Distribution of 10000 Samples using round method:
 -9: 0.01%
 -8: 0.01%
 -7: 0.01%
 -6: 0.01%
 -5: 0.04%
 -4: 0.3%
 -3: 1.53%
 -2: 6.7%
 -1: 22.81%
 0: 36.51%
 1: 23.4%
 2: 6.79%
 3: 1.42%
 4: 0.34%
 5: 0.09%
 6: 0.02%
 18: 0.01%


=========================================================================
Total Test Time: 0.5868 seconds

```
