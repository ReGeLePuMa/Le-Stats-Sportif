type ResultProps = {
  result: string; // Define the type of props you want to receive
};

const Result: React.FC<ResultProps> = ({ result }) => {
  return (
    <div>
      <h2>Result</h2>
      <p>{result}</p> {/* Access props inside the component */}
    </div>
  );
};

export default Result;