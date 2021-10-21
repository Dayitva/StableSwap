/**
 *
 * @param {Array<Number>} tokenPool
 * @param {Number} A
 * @param {Number} N_COINS
 * @returns {Number}
 */
function getD(tokenPool, A, N_COINS) {
  // tokenPool = [token1_amount, token2_amount];
  let S = tokenPool[0] + tokenPool[1];
  let Dprev = 0;

  let D = S;
  let Ann = A * N_COINS;
  let D_P = D;

  while (Math.abs(D - Dprev) > 1) {
    D_P = D;
    let x = 0;
    while (x < N_COINS) {
      D_P = (D_P * D) / (N_COINS * tokenPool[x]);
      x += 1;
    }
    Dprev = D;
    let D1 = (Ann * S + D_P * N_COINS) * D;
    let D2 = (Ann - 1) * D + (N_COINS + 1) * D_P;
    D = D1 / D2;
  }
  return D;
}

function getY(tokenPool, A, x, N_COINS) {
  // x is the amount that we want to exchange.
  // 1 and j are the index of tokens while exchanging from i -> j
  let D = getD(tokenPool, A, N_COINS);
  let c = D;
  let Ann = A * N_COINS;

  c = (D * D) / (x * N_COINS);
  c = (c * D) / (Ann * N_COINS);
  let b = x + D / Ann;

  let y_prev = 0;
  let y = D;

  while (Math.abs(y - y_prev) > 1) {
    y_prev = y;
    y = (y * y + c) / (2 * y + b - D);
  }

  return y;
}

function getDy(tokenPool, i, j, dx, A, N_COINS) {
  // From i to j `dx` amount of tokens.
  let x = tokenPool[i] + dx * 10 ** 9;
  let y = getY(tokenPool, A, x, N_COINS);
  let dy = tokenPool[j] - y;
  return (dy / 10 ** 9).toFixed(4);
}
let tokens = getDy([120000 * 10 ** 9, 80000 * 10 ** 9], 0, 1, 100, 4500, 2);
console.log(tokens);
