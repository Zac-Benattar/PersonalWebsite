import React from "react";

const ProgressBar = ({ progress }) => {
  const Parentdiv = {
    height: 30,
    width: "100%",
    backgroundColor: "rgb(193, 191, 191)",
    borderRadius: 40,
  };

  const Childdiv = {
    height: "100%",
    width: `${progress}%`,
    backgroundColor: "rgb(11, 150, 189)",
    borderRadius: 40,
    textAlign: "right",
  };

  const progresstext = {
    padding: 5,
    color: "white",
    fontWeight: 500,
  };

  return (
    <div style={Parentdiv}>
      <div style={Childdiv}>
        <span style={progresstext}>{`${progress}%`}</span>
      </div>
    </div>
  );
};

export default ProgressBar;
