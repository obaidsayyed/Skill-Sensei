export default function ScoreBar({ value }: { value: number }) {
  return <div className="score-bar"><i style={{ width: `${value}%` }} /></div>
}
