import git
import os


class GitManager:
    """
    A manager class to interact with Git repositories and retrieve file-related information.

    Methods:
    - get_all_files_in_directory(directory): Retrieves all files in a directory, excluding certain directories and hidden files.
    - get_local_files(directory=None, tree=None, ignored_file_beginnings=None): Retrieves local files in a directory or tree while filtering out ignored file beginnings.
    - get_files_content(directory): Retrieves the content of files in a directory.
    - get_commit_tree(directory): Retrieves the commit tree of a Git repository.
    """

    @staticmethod
    def get_all_files_in_directory(directory):
        """
        Retrieves all files in a directory, excluding certain directories and hidden files.

        Args:
        - directory (str): The directory path.

        Returns:
        - List[str]: List of paths to all files in the directory.
        """
        all_files = []
        for root, dirs, files in os.walk(directory):
            if 'venv' in dirs:
                dirs.remove('venv')

            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('__')]
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        return all_files

    @classmethod
    def get_local_files(cls, directory=None, tree=None, ignored_file_beginnings=None):
        """
        Retrieves local files in a directory or tree while filtering out ignored file beginnings.

        Args:
        - directory (str): The directory path.
        - tree: A tree representation (if available).
        - ignored_file_beginnings (List[str], optional): List of prefixes to ignore in file names. Defaults to None.

        Returns:
        - tuple: Tuple of filtered local files.
        """
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
        """
        Retrieves the content of files in a directory.

        Args:
        - directory (str): The directory path.

        Returns:
        - Dict[str, str]: Dictionary with file paths as keys and file contents as values.
        """
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
        """
        Retrieves the commit tree of a Git repository.

        Args:
        - directory (str): The directory path.

        Returns:
        - git.Tree: The commit tree of the Git repository.
        """
        repo = git.Repo(directory)
        return repo.head.commit.tree
