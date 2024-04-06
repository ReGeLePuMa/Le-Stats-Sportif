import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaHome } from "react-icons/fa";
import "../../index.css";

const Navbar = () => {
  const [isTapped, setIsTapped] = useState(true);
  const navigate = useNavigate();
  const scrollToTop = () => {
    navigate("/");
  };

  return (
    <div className="w-screen flex items-center justify-between p-4 bg-black text-white fixed top-0 z-20 overflow-x-hidden my-auto">
      <div>
        <button
          className={`flex items-center bg-${
            isTapped ? "black" : "white"
          } text-${
            isTapped ? "white" : "black"
          } text-2xl cursor-pointer  min-[700px]:hover:bg-white min-[700px]:hover:text-black rounded-lg min-[700px]:hover:scale-105 transition-all duration-300 p-4`}
          onClick={scrollToTop}
        >
          <FaHome className="mr-2" />
          <span>
            <span className="font-normal">LE ST</span>
            <span className="font-semibold">ATS SPORTIF</span>
          </span>
        </button>
      </div>
      <div className="hidden sm:flex items-center justify-end flex-1">
        <a
          href="https://ocw.cs.pub.ro/courses/asc/teme/tema1"
          target="_blank"
          rel="noopener noreferrer"
          className="nav-link cursor-pointer  hover:bg-white hover:text-black rounded-lg hover:scale-105 transition-all duration-300 text-2xl p-4 font-bold"
        >
          About
        </a>
      </div>
    </div>
  );
};

export default Navbar;
