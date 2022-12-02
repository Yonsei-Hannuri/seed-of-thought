export const round = (number, place) => {
  const placeMutiplier = 10 ** place;
  return Math.floor(number * placeMutiplier) / placeMutiplier;
};

export const currentTimeInSeconds = () => new Date().getTime() / 1000;
