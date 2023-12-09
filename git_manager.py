import git


class GitManager:
    @classmethod
    def get_local_files(cls, directory=None, tree=None, ignored_file_beginnings=None):
        if directory == tree is None:
            raise TypeError("Either directory or tree parameter has to be given")

        if ignored_file_beginnings is None:
            ignored_file_beginnings = ["."]

        newest_commit_tree = cls.get_commit_tree(directory) if tree is None else tree

        def ignored_files_filter(elem):
            for ignored_file_beginning in ignored_file_beginnings:
                if elem.name.startswith(ignored_file_beginning):
                    return False
            return True

        return tuple(filter(ignored_files_filter, newest_commit_tree))

    @classmethod
    def get_files_content(cls, directory):
        newest_commit_tree = cls.get_commit_tree(directory)
        files = cls.get_local_files(directory)
        file_contents = {}
        for f in files:
            blob = newest_commit_tree[f.name]
            content = blob.data_stream.read().decode()
            file_contents[f.path] = content
        return file_contents



    @staticmethod
    def get_commit_tree(directory):
        repo = git.Repo(directory)
        return repo.head.commit.tree
