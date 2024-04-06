import Video from '../../assets/video.mp4'
import Photo from '../../assets/image.jpg'
import "../../index.css"
import Result from '../Result/Result'
import { useEffect, useState } from 'react';

enum TaskType {
  STATES_MEAN = 1,
  STATE_MEAN = 2,
  BEST_5 = 3,
  WORST_5 = 4,
  GLOBAL_MEAN = 5,
  DIFFERENT_FROM_MEAN = 6,
  STATE_DIFFERENT_FROM_MEAN = 7,
  MEAN_BY_CATEGORY = 8,
  STATE_MEAN_BY_CATEGORY = 9
}

const questions = [
        'Percent of adults aged 18 years and older who have an overweight classification',
        'Percent of adults aged 18 years and older who have obesity',
        'Percent of adults who engage in no leisure-time physical activity',
        'Percent of adults who report consuming fruit less than one time daily',
        'Percent of adults who report consuming vegetables less than one time daily',
        'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
        'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
        'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
        'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
];

const states = [
  'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
  'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
  'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
  'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
  'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
  'Guam', 'Puerto Rico', 'District of Columbia', 'Virgin Islands'
];

const TASKS_ENDPOINTS: Record<TaskType, string> = {
  [TaskType.STATES_MEAN]: "/api/states_mean",
  [TaskType.STATE_MEAN]: "/api/state_mean",
  [TaskType.BEST_5]: "/api/best5",
  [TaskType.WORST_5]: "/api/worst5",
  [TaskType.GLOBAL_MEAN]: "/api/global_mean",
  [TaskType.DIFFERENT_FROM_MEAN]: "/api/diff_from_mean",
  [TaskType.STATE_DIFFERENT_FROM_MEAN]: "/api/state_diff_from_mean",
  [TaskType.MEAN_BY_CATEGORY]: "/api/mean_by_category",
  [TaskType.STATE_MEAN_BY_CATEGORY]: "/api/state_mean_by_category"
};

function Home(){

  const [selectedTask, setSelectedTask] = useState<TaskType | null>(null);
  const [selectedState, setSelectedState] = useState('');
  const [result, setResult] = useState('');

  const handleStateChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedState(event.target.value);
  }

    

  const handleTaskChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedTask(parseInt(event.target.value));
  };

  const stateOptions = states.map((state, index) => (
    <option key={index} value={state.toLowerCase().replace(/\s+/g, '-')}>
      {state}
    </option>
  ));

  const renderThirdDropdown = () => {
    if (selectedTask === TaskType.STATE_MEAN || selectedTask === TaskType.STATE_DIFFERENT_FROM_MEAN || selectedTask === TaskType.STATE_MEAN_BY_CATEGORY) {
      return (
        <select className="mb-4 px-4 py-2 border-2 border-black bg-white text-black rounded-lg border-none"
        onChange={handleStateChange}>
          <option value="">Select State</option>
          {stateOptions}
        </select>
      );
    }
    return null;
  };

  const capitalizeFirstLetter = (str: string) => {
    return str.replace(/\b\w/g, (char) => char.toUpperCase());
  }

  const taskOptions = Object.entries(TaskType).map(([key, value]) => {
    if (typeof value === 'number') {
      const label = key.replace(/_/g, ' ').toLowerCase();
      return (
        <option key={value} value={String(value)}>
          {capitalizeFirstLetter(label)}
        </option>
      );
    }
    return null;
  });
  
  const questionOptions = questions.map((question, index) => (
    <option key={index} value={`question-${index + 1}`}>
      {question}
    </option>
  ));

  const [selectedQuestion, setSelectedQuestion] = useState('Sel');

  const handleQuestionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedQuestion(event.target.value);
    const selectedLength = event.target.value.length
    document.getElementById('questionSelect')?.setAttribute('style', `width: ${selectedLength * 100}px;`);
  };

  const triggerQuestionChange = () => {
    const event = {
      target: {
        value: selectedQuestion
      }
    } as React.ChangeEvent<HTMLSelectElement>;
    handleQuestionChange(event);
  };

  useEffect(() => {
    triggerQuestionChange();
  }, []); 

  const resetForm = () => {
    setSelectedTask(null);
    setSelectedQuestion('Sel');
    setSelectedState('');
    setResult('');
  };

  const handleSubmit = () => {
    if (selectedTask && selectedQuestion != 'Sel') {
      if (selectedTask === TaskType.STATE_MEAN || selectedTask === TaskType.STATE_DIFFERENT_FROM_MEAN || selectedTask === TaskType.STATE_MEAN_BY_CATEGORY) {
        if (!selectedState) {
          console.error('State must be selected');
          return;
        }
      }
      const endpoint = TASKS_ENDPOINTS[selectedTask];
      if (endpoint) {
        fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ "question": selectedQuestion, "state": selectedState })
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          if (data.job_id) {
            setResult(data.job_id);
            resetForm();
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
      } else {
        console.error('Endpoint not found for selected task');
      }
    } else {
      console.error('Task and question must be selected');
    }
  };

  const RenderResultComponent = () => {
    if (result !== '') {
      return <Result result={result} />;
    }
    return null;
  };

  return (
    <div className="h-screen w-screen relative flex items-center justify-center mt-4 p-4">
        <video className="w-full h-screen object-cover absolute top-0 left-0" autoPlay loop muted playsInline poster={Photo}>
          <source src={Video} type="video/mp4" />
        </video>
    <div className="flex flex-col items-center w-full justify-center text-white z-10">
        <h1 className="text-9xl font-bold mb-8" style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)' }}>Le Stats Sportif</h1>

        <form className="flex flex-col justify-center items-center">
          <select
            className="mb-4 px-4 py-2 border-2 border-black bg-white text-black rounded-lg border-none"
            onChange={handleTaskChange}
            value={selectedTask || ''}
          >
            <option value="">Select Task</option>
            {taskOptions}
          </select>

          <select
            id="questionSelect"
            className="mb-4 px-4 py-2 border-2 border-black bg-white text-black rounded-lg border-none width-20"
            onChange={handleQuestionChange}
            value={selectedQuestion}
          >
            <option value="Sel">Select Question</option>
            {questionOptions}
          </select>

          {renderThirdDropdown()}

          <button type="submit" className="bg-white border border-black hover:border-white hover:bg-black hover:text-white text-black font-bold py-2 px-4 rounded-lg transition duration-300 ease-in-out"
          onClick={handleSubmit}>
            Submit
          </button>
        </form>
        <RenderResultComponent />
      </div>
  </div>
  )
}

export default Home