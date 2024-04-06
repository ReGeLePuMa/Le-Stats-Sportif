import { useEffect, useState } from "react";
import React from 'react';
type ResultProps = {
    result: string;
    taskType: number;
};


const Result: React.FC<ResultProps> = ({ result, taskType }) => {

    const BASE_URL = 'http://127.0.0.1:5000';
    const [data, setData] = useState({});
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${BASE_URL}/api/get_results/${result}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const jsonData = await response.json();
                if (jsonData.status === 'done') {
                    const dataArray = Object.entries(jsonData.data || {});
                    setData(dataArray);
                } else if (jsonData.status === 'running') {
                    setTimeout(fetchData, 500);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, [result]);
    return (
        <div className={`w-full ${[2, 3, 4, 5, 7].includes(taskType) ? 'h-screen' : 'h-full'} relative flex-grow bg-black flex items-center justify-center mt-20 p-4`}>
            <div className="text-center">
                <h2 className="text-5xl text-white font-bold my-4">Result</h2>
                <table className="table-auto">
                    <tbody>
                        {Object.entries(data).map(([state, mean]) => {
                            if (taskType === 8) {
                                let [stat, medie]: [string, number] = mean as [string, number];
                                stat = stat.replace("(", "").replace(")", "");
                                return (
                                    <tr key={state}>
                                        <td className="text-white px-4 py-2">{stat}</td>
                                        <td className="text-white px-4 py-2">{medie}</td>
                                    </tr>
                                );
                            }
                            if (taskType === 9) {
                                let [stat, medie]: [string, [string, number]] = mean as [string, [string, number]];

                                return (
                                    <div className="text-center">
                                        <h2 className="text-3xl text-white font-semibold my-4">{stat}</h2>
                                        {Object.entries(medie).map(([key, value]) => {
                                            let cheie = key.replace("(", "").replace(")", "");
                                            return (
                                                <tr key={key}>
                                                    <td className="text-white px-4 py-2">{cheie}</td>
                                                    <td className="text-white px-4 py-2">{value}</td>
                                                </tr>
                                            );
                                        })}
                                    </div>
                                );
                            }
                            let [stat, medie] = String(mean).split(",")
                            if (stat === "global_mean") {
                                stat = "Global Mean"
                            }

                            return (
                                <tr key={state}>
                                    <td className="text-white px-4 py-2">{stat}</td>
                                    <td className="text-white px-4 py-2">{medie}</td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
};


export default Result;