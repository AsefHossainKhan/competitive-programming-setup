use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    let test_case: usize = lines.next().unwrap().unwrap().trim().parse().unwrap();

    for _ in 0..test_case {
        lines.next(); // skip the line with the number of dishes
        let dishes_to_eat: Vec<usize> = lines
            .next()
            .unwrap()
            .unwrap()
            .trim()
            .split_whitespace()
            .map(|x| x.parse().unwrap())
            .collect();
        solve(dishes_to_eat);
    }
}

fn solve(input: Vec<usize>) {
    // max value from dishes to eat array
    let max_dish = input.iter().max().unwrap();
    // count how many times the max value appears in the array
    let count_max_dish = input.iter().filter(|&&x| x == *max_dish).count();
    println!("{}", count_max_dish);
}
