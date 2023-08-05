# Random Number Generator: RNG Storm Engine

Python API for the C++ Random library.

**RNG is not suitable for cryptography, but it could be perfect for other random stuff like data science, experimental programming, A.I. and games.**


*Recommended Installation:* `$ pip install RNG`


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
Raw Samples: False, True, False, True, True
Statistics of 1000 Samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.349
 Std Deviation: 0.4768924684102554
Distribution of 10000 Samples:
 False: 65.89%
 True: 34.11%


Integer Tests

Output Analysis: Random.randint(1, 6)
Typical Timing: 1157 ± 9 ns
Raw Samples: 4, 2, 4, 6, 5
Statistics of 1000 Samples:
 Minimum: 1
 Median: 3
 Maximum: 6
 Mean: 3.412
 Std Deviation: 1.6973912740252723
Distribution of 10000 Samples:
 1: 16.55%
 2: 16.65%
 3: 16.85%
 4: 16.33%
 5: 16.41%
 6: 17.21%

Output Analysis: random_int(1, 6)
Typical Timing: 63 ± 3 ns
Raw Samples: 3, 5, 6, 2, 4
Statistics of 1000 Samples:
 Minimum: 1
 Median: 3
 Maximum: 6
 Mean: 3.512
 Std Deviation: 1.6776980272595752
Distribution of 10000 Samples:
 1: 16.43%
 2: 16.55%
 3: 17.03%
 4: 16.59%
 5: 17.05%
 6: 16.35%

Output Analysis: Random.randrange(6)
Typical Timing: 813 ± 9 ns
Raw Samples: 2, 5, 5, 2, 2
Statistics of 1000 Samples:
 Minimum: 0
 Median: 2
 Maximum: 5
 Mean: 2.445
 Std Deviation: 1.6928794525425728
Distribution of 10000 Samples:
 0: 16.32%
 1: 16.48%
 2: 17.23%
 3: 17.25%
 4: 16.74%
 5: 15.98%

Output Analysis: random_below(6)
Typical Timing: 63 ± 1 ns
Raw Samples: 1, 1, 1, 5, 5
Statistics of 1000 Samples:
 Minimum: 0
 Median: 2
 Maximum: 5
 Mean: 2.441
 Std Deviation: 1.6611075456689366
Distribution of 10000 Samples:
 0: 16.61%
 1: 17.43%
 2: 16.96%
 3: 16.41%
 4: 16.16%
 5: 16.43%

Output Analysis: binomial(4, 0.5)
Typical Timing: 157 ± 1 ns
Raw Samples: 2, 3, 0, 2, 2
Statistics of 1000 Samples:
 Minimum: 0
 Median: 2
 Maximum: 4
 Mean: 1.987
 Std Deviation: 0.9898539340785644
Distribution of 10000 Samples:
 0: 6.36%
 1: 24.06%
 2: 37.95%
 3: 25.32%
 4: 6.31%

Output Analysis: negative_binomial(5, 0.75)
Typical Timing: 94 ± 3 ns
Raw Samples: 1, 0, 7, 1, 0
Statistics of 1000 Samples:
 Minimum: 0
 Median: 1
 Maximum: 11
 Mean: 1.681
 Std Deviation: 1.5157626913658142
Distribution of 10000 Samples:
 0: 23.74%
 1: 29.72%
 2: 22.46%
 3: 12.6%
 4: 6.7%
 5: 2.87%
 6: 1.25%
 7: 0.41%
 8: 0.12%
 9: 0.1%
 10: 0.01%
 11: 0.02%

Output Analysis: geometric(0.75)
Typical Timing: 63 ± 3 ns
Raw Samples: 0, 0, 2, 0, 0
Statistics of 1000 Samples:
 Minimum: 0
 Median: 0
 Maximum: 5
 Mean: 0.3
 Std Deviation: 0.6296001877353568
Distribution of 10000 Samples:
 0: 74.88%
 1: 18.76%
 2: 4.84%
 3: 1.11%
 4: 0.3%
 5: 0.1%
 6: 0.01%

Output Analysis: poisson(4.5)
Typical Timing: 94 ± 6 ns
Raw Samples: 3, 4, 5, 6, 2
Statistics of 1000 Samples:
 Minimum: 0
 Median: 4
 Maximum: 13
 Mean: 4.409
 Std Deviation: 2.141098620639251
Distribution of 10000 Samples:
 0: 1.09%
 1: 5.42%
 2: 11.25%
 3: 17.09%
 4: 18.69%
 5: 16.95%
 6: 12.62%
 7: 8.26%
 8: 4.51%
 9: 2.23%
 10: 1.22%
 11: 0.39%
 12: 0.17%
 13: 0.08%
 14: 0.02%
 16: 0.01%


Floating Point Tests

Output Analysis: Random.random()
Typical Timing: 32 ± 8 ns
Raw Samples: 0.6257220293192036, 0.1587843748525427, 0.5212498572433126, 0.7270672153308279, 0.8023202133212103
Statistics of 1000 Samples:
 Minimum: 4.0308304055991506e-05
 Median: (0.48855325419506757, 0.4911622083907684)
 Maximum: 0.9998519558812695
 Mean: 0.49175615021930663
 Std Deviation: 0.2889823765777354
Post-processor Distribution of 10000 Samples using round method:
 0: 49.54%
 1: 50.46%

Output Analysis: generate_canonical()
Typical Timing: 32 ± 8 ns
Raw Samples: 0.3919923329945272, 0.41818073403369316, 0.5300207819847063, 0.9375683114938821, 0.6855193554375915
Statistics of 1000 Samples:
 Minimum: 0.0006355869343482954
 Median: (0.5244474238636627, 0.5249991681457991)
 Maximum: 0.9973953180046232
 Mean: 0.5056732891617263
 Std Deviation: 0.28277163627596547
Post-processor Distribution of 10000 Samples using round method:
 0: 49.6%
 1: 50.4%

Output Analysis: random_float(0.0, 10.0)
Typical Timing: 32 ± 8 ns
Raw Samples: 1.0755298683940526, 5.892589290786171, 7.84103595022363, 8.919264937183272, 7.67034273465522
Statistics of 1000 Samples:
 Minimum: 0.0002999602651352327
 Median: (4.766424604483823, 4.767395816181031)
 Maximum: 9.992616736007315
 Mean: 4.93615923259551
 Std Deviation: 2.8523430944773938
Post-processor Distribution of 10000 Samples using floor method:
 0: 10.05%
 1: 10.54%
 2: 10.02%
 3: 10.69%
 4: 9.91%
 5: 9.73%
 6: 9.56%
 7: 9.16%
 8: 10.14%
 9: 10.2%

Output Analysis: Random.expovariate(1.0)
Typical Timing: 313 ± 8 ns
Raw Samples: 0.3403298785851924, 1.8695503980575472, 2.006131027716257, 0.17666073050768805, 0.6610628610218727
Statistics of 1000 Samples:
 Minimum: 0.0004599901011892646
 Median: (0.6938722809901098, 0.6955970987042109)
 Maximum: 7.48007341547659
 Mean: 1.0160539470048628
 Std Deviation: 1.0239717139175992
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 62.7%
 1: 23.65%
 2: 8.63%
 3: 2.9%
 4: 1.28%
 5: 0.56%
 6: 0.19%
 7: 0.06%
 8: 0.03%

Output Analysis: expovariate(1.0)
Typical Timing: 63 ± 1 ns
Raw Samples: 1.2158771218405877, 0.0006580149355547406, 3.3336627210354774, 0.16089317775744988, 0.9935061882820501
Statistics of 1000 Samples:
 Minimum: 0.0007610519578644641
 Median: (0.7041370625362988, 0.7055005266273829)
 Maximum: 7.331075483902089
 Mean: 0.9881086892747002
 Std Deviation: 0.9907673453845725
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.48%
 1: 23.21%
 2: 8.42%
 3: 3.01%
 4: 1.2%
 5: 0.44%
 6: 0.13%
 7: 0.07%
 8: 0.03%
 9: 0.01%

Output Analysis: Random.gammavariate(1.0, 1.0)
Typical Timing: 438 ± 4 ns
Raw Samples: 2.729062579347058, 0.8460431651735795, 0.5707596242192408, 0.09640018620563888, 3.3018018301521623
Statistics of 1000 Samples:
 Minimum: 5.528092390574849e-05
 Median: (0.6545835667826807, 0.6561126093591253)
 Maximum: 6.9687712625240055
 Mean: 0.9582681044027269
 Std Deviation: 0.9401762415257677
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.82%
 1: 22.54%
 2: 8.63%
 3: 3.34%
 4: 1.14%
 5: 0.36%
 6: 0.14%
 7: 0.01%
 8: 0.01%
 9: 0.01%

Output Analysis: gammavariate(1.0, 1.0)
Typical Timing: 63 ± 1 ns
Raw Samples: 2.706640164361005, 2.042397986007575, 0.250425671758887, 0.36636679900861036, 0.1464455029811769
Statistics of 1000 Samples:
 Minimum: 0.00011138974192093048
 Median: (0.7126399185829264, 0.7134140749165374)
 Maximum: 8.530397171800969
 Mean: 1.0007052803809535
 Std Deviation: 1.0316274116075677
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.44%
 1: 23.87%
 2: 7.99%
 3: 2.59%
 4: 1.33%
 5: 0.47%
 6: 0.12%
 7: 0.14%
 8: 0.05%

Output Analysis: Random.weibullvariate(1.0, 1.0)
Typical Timing: 407 ± 7 ns
Raw Samples: 0.07374858644737285, 1.3664831619431808, 0.7817519728248706, 1.4115697489361918, 0.5754479592305365
Statistics of 1000 Samples:
 Minimum: 0.0010137473074764325
 Median: (0.7095411577014754, 0.7123991158784878)
 Maximum: 8.43961718649647
 Mean: 1.0209661092377262
 Std Deviation: 1.0117055184612633
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 63.08%
 1: 23.69%
 2: 8.84%
 3: 2.71%
 4: 0.93%
 5: 0.48%
 6: 0.2%
 7: 0.03%
 8: 0.03%
 9: 0.01%

Output Analysis: weibullvariate(1.0, 1.0)
Typical Timing: 94 ± 7 ns
Raw Samples: 0.18397966560432863, 0.49710268748768144, 0.47829812464106797, 0.509331979488556, 3.589230749015156
Statistics of 1000 Samples:
 Minimum: 7.100867112417946e-05
 Median: (0.708364180038233, 0.7084554318294236)
 Maximum: 6.6947532502860465
 Mean: 1.0272201611242082
 Std Deviation: 1.0314859624044872
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 62.73%
 1: 23.43%
 2: 8.63%
 3: 3.2%
 4: 1.33%
 5: 0.4%
 6: 0.19%
 7: 0.08%
 9: 0.01%

Output Analysis: extreme_value(0.0, 1.0)
Typical Timing: 63 ± 8 ns
Raw Samples: -0.9780687130134689, 0.6627285831777763, 2.0079601426399467, 1.2427874837007744, -0.07851360634470904
Statistics of 1000 Samples:
 Minimum: -1.911303646052639
 Median: (0.3606568023487982, 0.36099195696436437)
 Maximum: 6.928327400208182
 Mean: 0.526610794341577
 Std Deviation: 1.1863383595339747
Post-processor Distribution of 10000 Samples using round method:
 -2: 1.15%
 -1: 18.26%
 0: 35.62%
 1: 25.48%
 2: 12.16%
 3: 4.73%
 4: 1.69%
 5: 0.64%
 6: 0.17%
 7: 0.07%
 8: 0.03%

Output Analysis: Random.gauss(5.0, 2.0)
Typical Timing: 594 ± 7 ns
Raw Samples: 4.628415583323791, 3.7432306486473044, 6.704729879486447, 4.688210045540809, 4.884067254851023
Statistics of 1000 Samples:
 Minimum: -1.8203839333270322
 Median: (5.016455632534685, 5.01871172130724)
 Maximum: 10.975720350483314
 Mean: 4.941882163203685
 Std Deviation: 1.9850250537994012
Post-processor Distribution of 10000 Samples using round method:
 -2: 0.06%
 -1: 0.29%
 0: 1.08%
 1: 3.09%
 2: 6.56%
 3: 12.73%
 4: 17.08%
 5: 18.98%
 6: 17.85%
 7: 11.86%
 8: 6.2%
 9: 2.97%
 10: 0.93%
 11: 0.26%
 12: 0.03%
 13: 0.02%
 14: 0.01%

Output Analysis: normalvariate(5.0, 2.0)
Typical Timing: 63 ± 3 ns
Raw Samples: 1.957603085512312, 5.5037188127943475, 4.308670511930885, 2.21386372724635, 6.176884548924962
Statistics of 1000 Samples:
 Minimum: -1.6166014290635278
 Median: (4.922056274725187, 4.926864815908566)
 Maximum: 11.000278139661937
 Mean: 4.946104803126899
 Std Deviation: 1.996222855683651
Post-processor Distribution of 10000 Samples using round method:
 -3: 0.01%
 -2: 0.06%
 -1: 0.21%
 0: 0.88%
 1: 2.41%
 2: 6.89%
 3: 12.01%
 4: 17.62%
 5: 19.61%
 6: 17.04%
 7: 12.5%
 8: 6.63%
 9: 2.98%
 10: 0.87%
 11: 0.24%
 12: 0.03%
 13: 0.01%

Output Analysis: Random.lognormvariate(1.6, 0.25)
Typical Timing: 813 ± 24 ns
Raw Samples: 7.518994321452813, 6.42276639612712, 7.237554653586027, 4.695984464925408, 4.938002246900153
Statistics of 1000 Samples:
 Minimum: 2.267642461387746
 Median: (4.828196870621551, 4.829928299046591)
 Maximum: 11.39003466260026
 Mean: 5.033850830621758
 Std Deviation: 1.3211016674997373
Post-processor Distribution of 10000 Samples using round method:
 2: 0.32%
 3: 8.07%
 4: 27.82%
 5: 30.11%
 6: 20.13%
 7: 8.67%
 8: 3.15%
 9: 1.31%
 10: 0.27%
 11: 0.11%
 12: 0.02%
 13: 0.02%

Output Analysis: lognormvariate(1.6, 0.25)
Typical Timing: 94 ± 7 ns
Raw Samples: 3.35955734270404, 3.6741748931906253, 6.08980572690649, 3.9583664144041166, 4.418629405871006
Statistics of 1000 Samples:
 Minimum: 2.0701375764643024
 Median: (4.928732354718039, 4.9298039510715475)
 Maximum: 11.077701461861214
 Mean: 5.10901866905853
 Std Deviation: 1.3612090753529316
Post-processor Distribution of 10000 Samples using round method:
 2: 0.26%
 3: 7.95%
 4: 26.68%
 5: 31.28%
 6: 19.93%
 7: 8.65%
 8: 3.58%
 9: 1.1%
 10: 0.4%
 11: 0.12%
 12: 0.03%
 13: 0.02%

Output Analysis: chi_squared(1.0)
Typical Timing: 125 ± 5 ns
Raw Samples: 0.7351338156642365, 0.10197043213874361, 0.0004479891839900254, 2.773185433186169, 0.47738197707610047
Statistics of 1000 Samples:
 Minimum: 5.55023621582499e-06
 Median: (0.3981406583528158, 0.3990955485821841)
 Maximum: 10.477883297941728
 Mean: 0.9496774391499728
 Std Deviation: 1.382725300404331
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 69.06%
 1: 15.73%
 2: 7.51%
 3: 3.62%
 4: 1.8%
 5: 1.02%
 6: 0.6%
 7: 0.39%
 8: 0.17%
 9: 0.1%

Output Analysis: cauchy(0.0, 1.0)
Typical Timing: 63 ± 7 ns
Raw Samples: 0.12047614285340622, -0.9382817547743436, 0.3364748723191148, 0.20318849864529762, -0.02046005641688962
Statistics of 1000 Samples:
 Minimum: -82.48897001919615
 Median: (0.056003268199336674, 0.060337734319287115)
 Maximum: 10415.411578016254
 Mean: 11.141540433195399
 Std Deviation: 329.92131299483765
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 26.58%
 1: 11.58%
 2: 5.94%
 3: 3.58%
 4: 3.22%
 5: 3.06%
 6: 3.58%
 7: 5.59%
 8: 10.85%
 9: 26.02%

Output Analysis: fisher_f(8.0, 8.0)
Typical Timing: 188 ± 7 ns
Raw Samples: 1.303940866020909, 1.773026236828557, 0.9229338358989495, 0.4377167383233721, 0.6064276514082172
Statistics of 1000 Samples:
 Minimum: 0.08680712657350184
 Median: (1.0202664046567236, 1.0222205156710489)
 Maximum: 11.317407630701402
 Mean: 1.3511294154299045
 Std Deviation: 1.1354558855010388
Post-processor Distribution of 10000 Samples using floor_mod_10 method:
 0: 50.01%
 1: 33.26%
 2: 9.48%
 3: 3.98%
 4: 1.66%
 5: 0.74%
 6: 0.43%
 7: 0.26%
 8: 0.11%
 9: 0.07%

Output Analysis: student_t(8.0)
Typical Timing: 157 ± 7 ns
Raw Samples: -0.5820353912666035, 1.2372497128657416, -1.5848056582854368, -1.52921491899218, -0.672592744581616
Statistics of 1000 Samples:
 Minimum: -4.1554943175974906
 Median: (-0.0003756534266611156, 0.0010336151855832448)
 Maximum: 5.0968059761295645
 Mean: -0.020289732107086456
 Std Deviation: 1.196691848347625
Post-processor Distribution of 10000 Samples using round method:
 -9: 0.01%
 -6: 0.02%
 -5: 0.1%
 -4: 0.33%
 -3: 1.52%
 -2: 6.5%
 -1: 22.88%
 0: 37.59%
 1: 22.74%
 2: 6.39%
 3: 1.57%
 4: 0.27%
 5: 0.07%
 6: 0.01%


=========================================================================
Total Test Time: 0.5913 seconds

```
