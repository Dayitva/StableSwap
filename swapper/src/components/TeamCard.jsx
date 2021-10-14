import React from "react";

function TeamCard({ imgSrc, imgAlt, twitterUsername }) {
  return (
    <a href={`https://twitter.com/${twitterUsername}`}>
      <div className="w-96">
        <div className="rounded-full overflow-hidden h-32 w-32 mx-auto">
          <img src={imgSrc} alt={imgAlt} className="w-full object-cover " />
        </div>
        <div className="">
          <h1 className="font-semibold text-xl text-center mt-2">{imgAlt}</h1>
        </div>
      </div>
    </a>
  );
}

export default TeamCard;
