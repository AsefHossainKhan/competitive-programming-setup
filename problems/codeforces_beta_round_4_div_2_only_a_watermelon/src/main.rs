use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    solve(input);
}

fn solve(input: String) {
    let input = input.trim();

    // Example parsing helpers (you'll expand later)
    let mut it = input.split_whitespace();

    // Example: read first number if needed
    let n: i32 = it.next().unwrap().parse().unwrap();

    if n % 2 == 0 && n > 2 {
        println!("YES");
    } else {
        println!("NO");
    }
}
