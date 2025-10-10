local config = {}
for line in io.lines("config/project_name.conf") do
  local key, value = line:match("^(%w+)%s*=%s*(.+)$")
  if key and value then
    value = value:gsub("\\n", "\\\\")
    tex.sprint("\\expandafter\\def\\csname " .. key .. "\\endcsname{" .. value .. "}")
  end
end

