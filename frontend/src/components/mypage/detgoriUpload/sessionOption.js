export default function SessionOption({info}) {
    return (
      <option value={info.id}>
        {info.week}주차: {info.title}
      </option>
    );
}