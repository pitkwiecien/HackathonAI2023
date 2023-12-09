import git
import os


class GitManager:
    @staticmethod
    def get_all_files_in_directory(directory):
        all_files = []
        for root, dirs, files in os.walk(directory):
            if 'venv' in dirs:
                dirs.remove('venv')

            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('__')]
            for file in files:
                file_path = os.path.join(root, file)
                # file_path = os.path.relpath(file_path, directory)
                all_files.append(file_path)
        return all_files

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
