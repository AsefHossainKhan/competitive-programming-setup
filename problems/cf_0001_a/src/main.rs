use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    solve(input);
}

fn solve(input: String) {
    println!("{}", input);
}
