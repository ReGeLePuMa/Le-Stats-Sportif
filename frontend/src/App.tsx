import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/NavBar/NavBar'
import Home from './components/Home/Home'
import Result from './components/Result/Result';
import Footer from './components/Footer/Footer';


function App() {
  const [result, setResult] = useState('');
  const [type, setType] = useState(0);
  return (
    <Router>
      <Navbar />
      <Routes>
      <Route path='/' element={<Home setResult={setResult} setType={setType} />} />
      <Route path='/result' element={<Result result={result} taskType={type} />} />
      </Routes>
      <Footer />
    </Router>

  );
}

export default App
