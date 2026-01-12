class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def header(text: str) -> str:
        """Formats text as header (purple)."""
        return f"{Colors.HEADER}{text}{Colors.ENDC}"

    @staticmethod
    def info(text: str) -> str:
        """Formats text as info (yellow)."""
        return f"{Colors.WARNING}{text}{Colors.ENDC}"

    @staticmethod
    def success(text: str) -> str:
        """Formats text as success (green)."""
        return f"{Colors.OKGREEN}{text}{Colors.ENDC}"
    
    @staticmethod
    def warning(text: str) -> str:
        """Formats text as warning (yellow)."""
        return f"{Colors.WARNING}{text}{Colors.ENDC}"

    @staticmethod
    def error(text: str) -> str:
        """Formats text as error (red bold)."""
        return f"{Colors.FAIL}{Colors.BOLD}{text}{Colors.ENDC}"
    
    @staticmethod
    def section(text: str) -> str:
        """Formats text as a section header with separator."""
        return f"\n{Colors.BOLD}{Colors.OKBLUE}--- {text} ---{Colors.ENDC}"
