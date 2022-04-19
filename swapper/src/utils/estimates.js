import config from "../config";

function getD(tokenPool, A, N_COINS) {
  // tokenPool = [token1_amount, token2_amount];
  let S = tokenPool[0] + tokenPool[1];
  if (S === 0) {
    return 0;
  }
  let Dprev = 0;

  let D = S;
  let Ann = A * N_COINS;

  while (Math.abs(D - Dprev) > 1) {
    let D_P = D;
    // console.log({ D, Dprev });
    D_P = D;

    D_P = (D_P * D) / (N_COINS * tokenPool[0]);
    D_P = (D_P * D) / (N_COINS * tokenPool[1]);

    Dprev = D;
    let D1 = (Ann * S + D_P * N_COINS) * D;
    let D2 = (Ann - 1) * D + (N_COINS + 1) * D_P;
    D = D1 / D2;
  }
  console.log("dy is all good");
  return D;
}

function getY(tokenPool, A, x, N_COINS) {
  // x is the amount that we want to exchange.
  // 1 and j are the index of tokens while exchanging from i -> j
  console.log("Before getD");
  let D = getD(tokenPool, A, N_COINS);
  console.log("After getD");
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

// const decimals = { 0: 18, 1: 6 };

function getDy(tokenPool, i, j, dx, A, N_COINS) {
  // From i to j `dx` amount of tokens.
  console.log("getDy", tokenPool, i, j, dx, A, N_COINS);
  let x = tokenPool[i] + dx;
  console.log(x);
  let y = getY(tokenPool, A, x, N_COINS);
  let dy = tokenPool[j] - y;
  console.log(dy);
  return (dy - (config.fee / 100) * dy).toFixed(5);
}

function estimateTokensByLp(tokenPool, _amount, lpSupply) {
  // let token_supply = tokenPool[0] + tokenPool[1];

  // let _x4 = 0;
  let tokenOut = {};

  // For first token.
  let val = tokenPool[0].multipliedBy(_amount).dividedToIntegerBy(lpSupply);
  // val /= 10 ** 18 / config.tokens[0].decimals;
  tokenOut[0] = val;

  val = tokenPool[1].multipliedBy(_amount).dividedToIntegerBy(lpSupply);
  // val /= 10 ** 18 / config.tokens[1].decimals;
  tokenOut[1] = val;

  return tokenOut;
}

export const estimateLP = (tokenPool, amount, token, A) => {
  console.log(
    tokenPool,
    amount,
    token.tokenId,
    A,
    "Value from estimated tokens"
  );
  let tokenSupplyInitial = tokenPool[0] + tokenPool[1];
  const D0 = getD(tokenPool, A, 2);

  let tokenId = token.tokenId;
  tokenPool[tokenId] = tokenPool[tokenId] + amount;
  const D1 = getD(tokenPool, A, 2);

  let lpAmount = (tokenSupplyInitial * (D1 - D0)) / D0;
  return lpAmount;
};
console.log(
  "Testing estimation of LP",
  estimateLP([99677, 100338], 100, { tokenId: 0 }, 85)
);

export { getD, getY, getDy, estimateTokensByLp };
