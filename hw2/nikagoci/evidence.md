# Evidence

## Golden test cases

I created five test cases for my Vigenère encryption tool.

| #   | Test                                              | Expected result                                              | Status      |
| --- | ------------------------------------------------- | ------------------------------------------------------------ | ----------- |
| 1   | Encrypt normal text with a valid key              | Text is encrypted correctly                                  | Not run yet |
| 2   | Encrypt text containing spaces and punctuation    | Letters are encrypted; spaces and punctuation stay unchanged | Not run yet |
| 3   | Encrypt text with uppercase and lowercase letters | Original letter case is preserved                            | Not run yet |
| 4   | Use an empty key                                  | The tool rejects the input and returns an error              | Not run yet |
| 5   | Send an extra `user_id` field                     | The tool rejects the unexpected field                        | Not run yet |

## CI results

**Successful run:**  
Link: To be added after the successful GitHub Actions run.

**Failed run:**  
Link: To be added after testing the weakened contract on a temporary branch.

## What I learned from the failed run

I will add this after running the failed test. I want to explain what happened when I weakened the contract and whether the tests caught the problem and blocked the pull request.
