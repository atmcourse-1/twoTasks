const exist = (board, word) => {
  if (board.length === 0) return false;

  const height = board.length;
  const width = board[0].length;
  const dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]];

  const search = (x, y, k) => {
    if (board[x][y] !== word[k]) return false;
    if (k === word.length - 1) return true;

    board[x][y] = '*'; // mark as visited
    for (const [dx, dy] of dirs) {
      const i = x + dx;
      const j = y + dy;
      if (i >= 0 && i < height && j >= 0 && j < width) {
        if (search(i, j, k + 1)) return true;
      }
    }
    board[x][y] = word[k]; // reset
    return false;
  };

  for (let i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      if (search(i, j, 0)) return true;
    }
  }

  return false;
};

const testWord = 'ppt';

console.log(exist(board, testWord));