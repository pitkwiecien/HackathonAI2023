class CodeSplitter:
    def __init__(self, content, split_required=True):
        self.content = content
        if split_required:
            self.content = self.content.splitlines()

    def split(self):
        chunks = []
        new_chunk = ""
        for line in self.content:
            if line.strip() != "":
                if line[0] == " " or new_chunk == "":
                    new_chunk += line + "\n"
                else:
                    chunks.append(new_chunk)
                    new_chunk = line + "\n"
        if new_chunk != "":
            chunks.append(new_chunk)
        return chunks
