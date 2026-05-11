```rust
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    // let n: usize = lines.next().unwrap().unwrap().trim().parse().unwrap();
    let n: usize = lines.next().unwrap().unwrap().trim().parse().unwrap();

    for _ in 0..n {
        let word = lines.next().unwrap().unwrap().trim().to_string();
        solve(word);
    }
}

fn solve(input: String) {
    println!("{}", input);
}
```
