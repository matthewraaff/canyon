use std::cmp::{max, min};

struct Node {
    value: i32,
    children: Vec<Node>,
}

impl Node {
    fn is_terminal(&self) -> bool {
        self.children.is_empty()
    }

    fn value(&self) -> i32 {
        self.value
    }

    fn children(&self) -> &Vec<Node> {
        &self.children
    }
}

fn minimax(node: &Node, depth: i32, maximising_player: bool) -> i32 {
    if depth == 0 || node.is_terminal() {
        return node.value();
    }
    if maximising_player {
        let mut value = i32::MIN;
        for child in node.children() {
            value = max(value, minimax(child, depth - 1, false));
        }
        return value;
    } else {
        let mut value = i32::MAX;
        for child in node.children() {
            value = min(value, minimax(child, depth - 1, true));
        }
        return value;
    }
}

fn main() {
    println!("hello world");
}

// git test
