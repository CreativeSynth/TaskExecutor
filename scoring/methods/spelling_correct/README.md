# spelling_correct

## generate_diff(before, after)
* generates a list of differences in two strings
```python
before = '첫째, 부모님께 존댓말을 사용하는 것 입니다. 부모님은 웃어른이기 때문에 존댓말을 사용해야 합니다. 어떤 아이들은 부탁하거나 잘못했을때에만 존댓말을 쓰는데 그러지 않고 항상 웃어른인 부모님께는 존댓말을 사용해야 합니다.'
after = '첫째, 부모님께 존댓말을 사용하는 것입니다. 부모님은 웃어른이기 때문에 존댓말을 사용해야 합니다. 어떤 아이들은 부탁하거나 잘못했을 때에만 존댓말을 쓰는데 그러지 않고 항상 웃어른인 부모님께는 존댓말을 사용해야 합니다.'
print(generate_diff(before, after))
# [['것 입니다.', '것입니다.'], ['잘못했을때에만', '잘못했을 때에만']]
```

## How to evaluate?
* Refer to the paper: [Evaluating GPT-3.5 and GPT-4 on Grammatical Error Correction for Brazilian Portuguese](https://arxiv.org/pdf/2306.15788.pdf)
* Calculate $F_{0.5}$ score:
$$
F_{0.5} = \frac{ \left( 1 + {0.5}^2 \right) \times R \times P}{R + {0.5}^2 \times P}
$$

* Why not $F_1$ score?
    > When a grammar checker is put into actual use, it is important that its proposed corrections are highly accurate in order to gain user acceptance. Neglecting to propose a correction is not as bad as proposing an erroneous correction.